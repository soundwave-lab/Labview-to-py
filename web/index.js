//配列定義
var input=new Array(18);

var axis1,axis2,axis3;


//指定した保存先・ファイル名表示
document.getElementById('selectFile').addEventListener('click',async()=>{
   document.getElementById('selectFile').innerText=await eel.selectFile()();
});

// //軸設定のチェック
// function check_axis(){
//   let axis1=document.querySelector('[name="set1stAxis"]').value
//   let axis2=document.querySelector('[name="set2ndAxis"]').value
//   let axis3=document.querySelector('[name="set3rdAxis"]').value
//   if(axis1==axis2 || axis2==axis3 ||axis1==axis3){
//     console.log("change");
//     //document.getElementById("setAxis").style.backgroundColor="red";
//     document.getElementById("set1stAxis").style.backgroundColor="#FADBDA";
//     document.getElementById("set2ndAxis").style.backgroundColor="#FADBDA";
//     document.getElementById("set3rdAxis").style.backgroundColor="#FADBDA";
//   }else{
//     //document.getElementById("setAxis").style.backgroundColor="transparent";
//     console.log("none");
//     document.getElementById("set1stAxis").style.backgroundColor="transparent";
//     document.getElementById("set2ndAxis").style.backgroundColor="transparent";
//     document.getElementById("set3rdAxis").style.backgroundColor="transparent";
//     }
// }

//x-y-zなどの表記からそれぞれの軸の数字へ
function setAxis(axes){
    if(axes=="x-y-z"){
        axis1=1;
        axis2=2;
        axis3=3;
    }
    else if(axes=="x-z-y"){
        axis1=1;
        axis2=3;
        axis3=2;
    }
    else if(axes=="y-x-z"){
        axis1=2;
        axis2=1;
        axis3=3;
    }
    else if(axes=="y-z-x"){
        axis1=2;
        axis2=3;
        axis3=1;
    }
    else if(axes=="z-x-y"){
        axis1=3;
        axis2=1;
        axis3=2;
    }
    else{
        axis1=3;
        axis2=2;
        axis3=1;
    }
}

 
//変数をJSからPythonへ
var startButton=document.getElementById('start')
var stopButton=document.getElementById('stop')
var start_count=0
var stop_count=0

async function process(){
         eel.start_threading()
         var status=await eel.check()(); 
         //send_dataの処理を待つ
         if(status=="go"){
            //  await eel.reset()();
            //  startButton.removeAttribute("disabled"); //ボタン活性化
            //  stopButton.setAttribute("disabled", true); //ボタン非活性化
            //  startButton.innerText="START";
            //  stopButton.innerText="STOP";
            start_count=0;
         }
         else if(status=="finish"){
            await eel.stop_check_threading()(); //スレッドが終了しているかチェック
            startButton.removeAttribute("disabled"); //ボタン活性化
            stopButton.setAttribute("disabled", true); //ボタン非活性化
            startButton.innerText="START";
            stopButton.innerText="STOP";
            start_count=0;
         }
         
         else if(status=="suspending"){
            await eel.stop_check_threading()(); //スレッドが終了しているかチェック
            startButton.removeAttribute("disabled"); //ボタン活性化
            stopButton.removeAttribute("disabled");
            startButton.innerText="Resume";
            stopButton.innerText="STOP";
            start_count=1;
         }
        
};

startButton.addEventListener('click',()=>{
         startButton.setAttribute("disabled", true);　//ボタン非活性化
         stopButton.removeAttribute("disabled"); 
         startButton.innerText="Running"
         stopButton.innerText="Suspend"
         
        if(start_count==0){ //最初のスタートだけ実行
         //値を代入
         var axes=document.querySelector('[name="setAxis"]').value;
         setAxis(axes);
         input[0]=document.querySelector('[name="lowSpeed"]').value;
         input[1]=document.querySelector('[name="highSpeed"]').value;
         input[2]=document.querySelector('[name="3dgpib"]').value;
         input[3]=axis1;
         input[4]=axis2;
         input[5]=axis3;
         input[6]=document.querySelector('[name="intervalTime"]').value;
         input[7]=document.querySelector('[name="1stAxisPulse"]').value;
         input[8]=document.querySelector('[name="2ndAxisPulse"]').value;
         input[9]=document.querySelector('[name="3rdAxisPulse"]').value;
         input[10]=document.querySelector('[name="1stAxisPoint"]').value;
         input[11]=document.querySelector('[name="2ndAxisPoint"]').value;
         input[12]=document.querySelector('[name="3rdAxisPoint"]').value;
         input[13]=document.querySelector('[name="measure1"]').value;
         input[14]=document.querySelector('[name="measure2"]').value;
         input[15]=document.querySelector('[name="measure3"]').value;
         input[16]=document.querySelector('[name="measure4"]').value;
         input[17]=document.querySelector('[name="oscilogpib"]').value;
         eel.send_data(input)();
        }
        
        if(start_count==1){ //一時停止の時だけ実行
            eel.reset()();
        }
        
         process();
        });
         

//STOPを押したら実行（一時停止 or ストップ）
stopButton.addEventListener('click',async()=>{
   if(start_count==0){ //動作中から一時停止へ
        stopButton.setAttribute("disabled", true);
        await eel.suspend()();
        process();
    }
   else if(start_count==1){ //一時停止中のSTOP押したときの処理
        stopButton.setAttribute("disabled", true);
        await eel.stop()();
        start_count=0
        process();
    }
});

eel.expose(finish)
function finish(){ //eelの中でeel動かない
        process();
}

//現在位置を返す
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