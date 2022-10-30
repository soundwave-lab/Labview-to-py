//配列定義
var input=new Array(17);

//指定した保存先・ファイル名表示
document.getElementById('selectFile').addEventListener('click',async()=>{
   document.getElementById('selectFile').innerText=await eel.selectFile()();
});
 
//変数をJSからPythonへ
document.getElementById('start').addEventListener('click',async()=>{
         input[0]=document.querySelector('[name="lowSpeed"]').value
         input[1]=document.querySelector('[name="highSpeed"]').value
         input[2]=document.querySelector('[name="3dgpib"]').value
         input[3]=document.querySelector('[name="setAxis"]').value
         input[4]=document.querySelector('[name="intervalTime"]').value
         input[5]=document.querySelector('[name="1stAxisPulse"]').value
         input[6]=document.querySelector('[name="2ndAxisPulse"]').value
         input[8]=document.querySelector('[name="3rdAxisPulse"]').value
         input[9]=document.querySelector('[name="1stAxisPoint"]').value
         input[10]=document.querySelector('[name="2ndAxisPoint"]').value
         input[11]=document.querySelector('[name="3rdAxisPoint"]').value
         input[12]=document.querySelector('[name="measure1"]').value
         input[13]=document.querySelector('[name="measure2"]').value
         input[14]=document.querySelector('[name="measure3"]').value
         input[15]=document.querySelector('[name="measure4"]').value
         input[16]=document.querySelector('[name="oscilogpib"]').value
   await eel.send_data(input);
});