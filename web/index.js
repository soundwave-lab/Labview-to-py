//配列定義
var input=new Array(18);

//指定した保存先・ファイル名表示
document.getElementById('selectFile').addEventListener('click',async()=>{
   document.getElementById('selectFile').innerText=await eel.selectFile()();
});

//軸設定のチェック
function check_axis(){
   let axis1=document.querySelector('[name="set1stAxis"]').value
   let axis2=document.querySelector('[name="set2ndAxis"]').value
   let axis3=document.querySelector('[name="set3rdAxis"]').value
   if(axis1==axis2 || axis2==axis3 ||axis1==axis3){
    console.log("change");
    //document.getElementById("setAxis").style.backgroundColor="red";
    document.getElementById("set1stAxis").style.backgroundColor="#FADBDA";
    document.getElementById("set2ndAxis").style.backgroundColor="#FADBDA";
    document.getElementById("set3rdAxis").style.backgroundColor="#FADBDA";
   }else{
    //document.getElementById("setAxis").style.backgroundColor="transparent";
    console.log("none");
    document.getElementById("set1stAxis").style.backgroundColor="transparent";
    document.getElementById("set2ndAxis").style.backgroundColor="transparent";
    document.getElementById("set3rdAxis").style.backgroundColor="transparent";
    }
}

 
//変数をJSからPythonへ
document.getElementById('start').addEventListener('click',async()=>{
         input[0]=document.querySelector('[name="lowSpeed"]').value
         input[1]=document.querySelector('[name="highSpeed"]').value
         input[2]=document.querySelector('[name="3dgpib"]').value
         input[3]=document.querySelector('[name="set1stAxis"]').value
         input[4]=document.querySelector('[name="set2ndAxis"]').value
         input[5]=document.querySelector('[name="set3rdAxis"]').value
         input[6]=document.querySelector('[name="intervalTime"]').value
         input[7]=document.querySelector('[name="1stAxisPulse"]').value
         input[8]=document.querySelector('[name="2ndAxisPulse"]').value
         input[9]=document.querySelector('[name="3rdAxisPulse"]').value
         input[10]=document.querySelector('[name="1stAxisPoint"]').value
         input[11]=document.querySelector('[name="2ndAxisPoint"]').value
         input[12]=document.querySelector('[name="3rdAxisPoint"]').value
         input[13]=document.querySelector('[name="measure1"]').value
         input[14]=document.querySelector('[name="measure2"]').value
         input[15]=document.querySelector('[name="measure3"]').value
         input[16]=document.querySelector('[name="measure4"]').value
         input[17]=document.querySelector('[name="oscilogpib"]').value
   await eel.send_data(input);
});

//STOPを押したら実行（ストップ）
document.getElementById('stop').addEventListener('click',async()=>{
   await eel.stop()();
});

eel.expose(change_current_point)
function change_current_point(axis,point){
   if(axis==1){
   document.getElementById('1stAxisCPoint').innerText=point;
   }
   else if(axis==2){
   document.getElementById('2ndAxisCPoint').innerText=point;
   }
   else if(axis==3){
   document.getElementById('3rdAxisCPoint').innerText=point;
   }
   else{
   console.log("no set")
   }
};