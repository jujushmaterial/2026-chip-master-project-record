#!/usr/bin/env python3
"""Offline H2 package checks; synthetic values never represent TCAD results."""
from pathlib import Path
import tempfile, csv, importlib.util, py_compile, re, os, contextlib, io
import numpy as np

ROOT=Path(__file__).resolve().parent


def check_syntax():
    import ast
    # Sentaurus SWB preprocesses all @tokens@ before Python execution.
    token_re=re.compile(r'@(?:node(?:\|-[0-9]+)?|Mask|VBD_V|PEB_BIAS_V|SCR_BIAS_V)@')
    preprocessed={
        '@node|-4@':'7','@node|-1@':'12','@node@':'11',
        '@Mask@':'13.0','@VBD_V@':'15.0','@PEB_BIAS_V@':'14.985',
        '@SCR_BIAS_V@':'14.812',
    }
    for f in (ROOT/'H2_compare_cases.py',ROOT/'H2_prepare_decks.py',ROOT/'11_H2_EField_SVisualPy.py',ROOT/'13_H2_CathodePath_SVisualPy.py'):
        s=f.read_text(encoding='utf-8')
        for k,v in preprocessed.items():s=s.replace(k,v)
        assert not token_re.search(s),f'{f.name}: SWB preprocessor tokens left behind'
        ast.parse(s,filename=str(f))
    assert (ROOT/'12_H2_CathodePath_SDevice.cmd').read_text().count('Goal { Name="substrate" Voltage=-0.30 }')==1
    csv_path=ROOT/'H2_SWB_6cases_15Params.csv'
    with csv_path.open(newline='') as stream:r=list(csv.DictReader(stream))
    assert len(r)==6 and all(len(z)==15 for z in r)
    assert [float(z['Mask']) for z in r]==[16.3,14.0,13.0,12.5,12.2,12.0]
    assert all(all(z[key]==r[0][key] for key in r[0] if key!='Mask') for z in r)
    return True


def test_results():
    spec=importlib.util.spec_from_file_location('h2compare',ROOT/'H2_compare_cases.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    wanted=['Mask_um','VBD_V','INear_pAum2','Icommon_pAum2','DarkReduction_Near_pct',
      'DarkReduction_Common_pct','Ecenter_kVcm','ESTI5_kVcm','EMask_kVcm','EMask_r_um',
      'AvalMask_cm3s','ForwardI_RelativeP0','CathodeConnectivity','PEBRisk']
    assert list(mod.OUTPUT_COLUMNS)==wanted
    with tempfile.TemporaryDirectory() as tmp:
      base=Path(tmp);r=[]
      for i, mask in enumerate([16.3,14,13,12.5,12.2,12]):
        fold=base/str(i);fold.mkdir()
        vbd=15.0+0.10*i
        dark=fold/'dark.txt';dark.write_text('I_density_at_percentBelowVBD_A_per_um2='+str(1e-10*(1.0-0.05*i))+'\nDark_OK=1\n')
        # This tests only the aggregation formula and mandatory fields.
        iv=fold/'iv.csv';iv.write_text('ReverseBias_V,AbsAnodeCurrent_A\n0,1e-9\n14,2e-8\n15.5,3e-8\n')
        ef=fold/'field.txt';ef.write_text(f'Evaluation=PEB\nMask_um={mask}\nVBD_V={vbd}\nH2_error_cuts=0\nH2_valid_cuts=150\nE_Center_kVcm=400\nE_STI5_kVcm={350+i}\nE_Mask_kVcm=420\nE_Mask_r_um={mask}\nAval_Mask_cm3s=1000000\n')
        cn=fold/'conn.txt';cn.write_text(f'Mask_um={mask}\nH2_FWD_Data_OK=1\nFWD_I_cathode_0p30_A={1e-8*(1-0.03*i)}\nFWD_KCL_residual_0p30=0.0001\n')
        r.append({'Mask':mask,'VBD_V':vbd,'dark_iv_csv':iv,'dark_metrics':dark,'field_metrics':ef,'conn_metrics':cn,'CathodeConnectivity':'','PEBRisk':''})
      manifest=base/'manifest.csv'
      with manifest.open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=r[0].keys());wr.writeheader();wr.writerows(r)
      result=base/'results.csv';rows,volts=mod.analyze(manifest,result)
      with result.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);cols=list(reader.fieldnames);allrows=list(reader)
      assert cols==wanted and len(allrows)==6
      assert rows[0]['DarkReduction_Near_pct']==0 and rows[0]['DarkReduction_Common_pct']==0
      assert rows[0]['ForwardI_RelativeP0']==1
      assert abs(rows[1]['DarkReduction_Near_pct']-5.0)<1e-10
      assert rows[0]['PEBRisk']=='REVIEW_REQUIRED' and rows[0]['CathodeConnectivity']=='REVIEW_REQUIRED'
      # Force one case's cut scan incomplete -> no comparison CSV created.
      bad=(base/'1'/'field.txt');bad.write_text(bad.read_text().replace('H2_error_cuts=0','H2_error_cuts=1'))
      output=base/'bad.csv'
      try:mod.analyze(manifest,output)
      except ValueError as exc:assert 'incomplete field' in str(exc)
      else:raise AssertionError('Did not reject failed field sampling')
      assert not output.exists()
      # Restore and test manually reviewed labels pass through only when supplied.
      bad.write_text(bad.read_text().replace('H2_error_cuts=1','H2_error_cuts=0'))
      r[0]['CathodeConnectivity']='CONNECTED';r[0]['PEBRisk']='INCONCLUSIVE'
      with manifest.open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=r[0].keys());wr.writeheader();wr.writerows(r)
      rows,volts=mod.analyze(manifest,base/'manual.csv')
      assert rows[0]['CathodeConnectivity']=='CONNECTED' and rows[0]['PEBRisk']=='INCONCLUSIVE'
    return True


def test_field_mock():
    """Exercise both SCR & PEB cuts with duplicate-name rejection in fake SVisual."""
    class FakeVisual:
        def __init__(self):self.data={};self.names=set();self.count=0
        def load_file(self,f,name):self.data[name]={'file':f}
        def create_plot(self,name,dataset):return name
        def create_cutline(self,direction,at,dataset=None,plot=None,materials=None,name=None):
            if not materials or materials!=['Silicon']:raise ValueError('missing filter')
            if name in self.names:raise RuntimeError('duplicate name '+name)
            self.names.add(name);self.count+=1
            r=float(at)
            self.data[name]={
                'Y':np.asarray([0.32,0.42,0.50,0.65,0.9]),
                'AbsElectricField':np.asarray([100000,400000*(1+0.02*r),150000,120000,50000]),
                'AvalancheGeneration':np.asarray([1e10,5e11*(1+0.01*r),1e11,1e10,1e9]),
            }
            return name
        def list_variables(self,dataset):return list(self.data[dataset].keys())
        def get_variable_data(self,varname,dataset):return self.data[dataset][varname]
    template=(ROOT/'11_H2_EField_SVisualPy.py').read_text()
    template=(template.replace('@node|-4@','7').replace('@node@','11')
      .replace('@Mask@','13.0').replace('@VBD_V@','15.0')
      .replace('@PEB_BIAS_V@','14.985').replace('@SCR_BIAS_V@','14.812'))
    with tempfile.TemporaryDirectory() as t:
      cwd=os.getcwd();os.chdir(t)
      try:
        for tag in ('SCR','PEB'):Path('n7_'+tag+'_des.tdr').touch()
        sv=FakeVisual();g={'sv':sv,'__name__':'__main__'}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(template,'11_H2_EField_SVisualPy.py','exec'),g,g)
        assert sv.count>100 and sv.count==len(sv.names)
        for tag in ('SCR','PEB'):
          assert Path(f'n11_H2_{tag}_metrics.txt').exists()
          assert Path(f'n11_H2_{tag}_samples.csv').exists()
          assert 'H2_error_cuts=0' in Path(f'n11_H2_{tag}_metrics.txt').read_text()
      finally:os.chdir(cwd)
    return True

if __name__=='__main__':
    for func in (check_syntax,test_results,test_field_mock):
        assert func()
        print('PASS',func.__name__)
    print('All H2 OFFLINE tests passed. Sentaurus actual run NOT tested.')
