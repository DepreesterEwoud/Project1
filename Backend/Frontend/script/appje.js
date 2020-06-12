const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let html_lichten;

const listenToUI= function(){
  //console.log("UI");
  const knoppen_lichten = document.querySelectorAll(".js-licht-btn");
  const knoppen_bijbaanlichten = document.querySelectorAll(".js-bijbaanlicht-btn");
  const knoppen_autoverkeer = document.querySelectorAll(".js-lichten-auto");
  const knoppen_straatlichten = document.querySelectorAll(".js-straatlichten");

  for(const knop of knoppen_lichten){
    knop.addEventListener("click", function(){
      const id = this.getAttribute("data-verkeerslicht");
      console.log(id);
      socket.emit("F2B_verander_licht", {verkeerslichtid: id});
    })
  }
  for(const knop of knoppen_bijbaanlichten){
    knop.addEventListener("click", function(){
      const id = this.getAttribute("data-bijbaanverkeerslicht");
      console.log(id);
      socket.emit("F2B_verander_bijbaanlicht", {verkeerslichtid: id});
    })
  }
  for(const knop of knoppen_autoverkeer){
    knop.addEventListener("click", function(){
      const id = this.getAttribute("data-autoverkeer");
      console.log(id);

      socket.emit("F2B_verander_autoverkeer", {autoverkeerslichten: id});
    })
  }
  for(const knop of knoppen_straatlichten){
    knop.addEventListener("click", function(){
      const id = this.getAttribute("data-straatlichten");
      console.log(id);

      socket.emit("F2B_verander_straatverlichting", {straatverlichting: id});
    })
  }
};

const listenToSocket = function(){
  console.log("data");
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    console.log();
  });
  socket.on("B2F_switch_light",function(data){
    //console.log("light");
    //console.log(data.licht1.verkeerslichtid);
    if(data.licht2.verkeerslichtid == 1){
      html_lichten.innerHTML = `<div class="lichten">
      <div class="circle red" color="red"></div>
      <div class="circle" color="yellow"></div>
      <div class="circle" color="green"></div>
      </div>`;
    }
    else if(data.licht2.verkeerslichtid == 2){
      html_lichten.innerHTML = `<div class="lichten">
      <div class="circle" color="red"></div>
      <div class="circle yellow" color="yellow"></div>
      <div class="circle" color="green"></div>
      </div>`;
    }
    else{
      html_lichten.innerHTML = `<div class="lichten">
      <div class="circle" color="red"></div>
      <div class="circle" color="yellow"></div>
      <div class="circle green" color="green"></div>
      </div>`;
    }
    if(data.licht1.verkeerslichtid == 1){
      html_lichten3.innerHTML = `<div class="lichten">
      <div class="circle red" color="red"></div>
      <div class="circle" color="yellow"></div>
      <div class="circle" color="green"></div>
      </div>`;
    }
    else if(data.licht1.verkeerslichtid == 2){
      html_lichten3.innerHTML = `<div class="lichten">
      <div class="circle" color="red"></div>
      <div class="circle yellow" color="yellow"></div>
      <div class="circle" color="green"></div>
      </div>`;
    }
    else{
      html_lichten3.innerHTML = `<div class="lichten">
      <div class="circle" color="red"></div>
      <div class="circle" color="yellow"></div>
      <div class="circle green" color="green"></div>
      </div>`;
    }
  });
  socket.on("B2F_verander_licht",function(data){
    //console.log("light");
    //console.log(data);
    if(data.licht1.verkeerslichtid == 1){
      html_lichten.innerHTML = `<div class="lichten">
      <div class="circle red" color="red"></div>
      <div class="circle" color="yellow"></div>
      <div class="circle" color="green"></div>
      </div>`;
    }
    else if(data.licht1.verkeerslichtid == 2){
      html_lichten.innerHTML = `<div class="lichten">
      <div class="circle" color="red"></div>
      <div class="circle yellow" color="yellow"></div>
      <div class="circle" color="green"></div>
      </div>`;
    }
    else{
      html_lichten.innerHTML = `<div class="lichten">
      <div class="circle" color="red"></div>
      <div class="circle" color="yellow"></div>
      <div class="circle green" color="green"></div>
      </div>`;
    }
  });
  socket.on("B2F_verander_bijbaanlicht",function(data){
    //console.log("light");
    console.log(data);
    if(data.licht2.verkeerslichtid == 1){
      html_lichten3.innerHTML = `<div class="lichten">
      <div class="circle red" color="red"></div>
      <div class="circle" color="yellow"></div>
      <div class="circle" color="green"></div>
      </div>`;
    }
    else if(data.licht2.verkeerslichtid == 2){
      html_lichten3.innerHTML = `<div class="lichten">
      <div class="circle" color="red"></div>
      <div class="circle yellow" color="yellow"></div>
      <div class="circle" color="green"></div>
      </div>`;
    }
    else{
      html_lichten3.innerHTML = `<div class="lichten">
      <div class="circle" color="red"></div>
      <div class="circle" color="yellow"></div>
      <div class="circle green" color="green"></div>
      </div>`;
    }
  });
  socket.on("B2F_ldrwaarde",function(data){
    console.log(data);
  });
}


const getLichten = function(ID){
  
  console.info("Historiek ophalen uit JSON");
  const elementByType = handleData(
    `http://192.168.1.22:5000/api/v1/verkeerslichten/${ID}`,
    Showlichten
    )
}
const getAndereLichten = function(ID){
  
  console.info("Historiek ophalen uit JSON");
  const elementByType = handleData(
    `http://192.168.1.22:5000/api/v1/verkeerslichten/${ID}`,
    ShowAndereLichten
    )
}

const Showlichten = function(data){
  console.log(data.status.verkeerslichtid);
  let html_string_lichten = ``;
  if(data.status.verkeerslichtid == 1){
    html_lichten.innerHTML = `<div class="lichten">
    <div class="circle red" color="red"></div>
    <div class="circle" color="yellow"></div>
    <div class="circle" color="green"></div>
    </div>`;
    html_lichten2.innerHTML = `<div class="lichten">
    <div class="circle red" color="red"></div>
    <div class="circle" color="yellow"></div>
    <div class="circle" color="green"></div>
    </div>`;
  }
  else if(data.status.verkeerslichtid == 2){
    html_lichten.innerHTML = `<div class="lichten">
    <div class="circle" color="red"></div>
    <div class="circle yellow" color="yellow"></div>
    <div class="circle" color="green"></div>
    </div>`;
    html_lichten2.innerHTML = `<div class="lichten">
    <div class="circle" color="red"></div>
    <div class="circle yellow" color="yellow"></div>
    <div class="circle" color="green"></div>
    </div>`;
  }
  else{
    html_lichten.innerHTML = `<div class="lichten">
    <div class="circle" color="red"></div>
    <div class="circle" color="yellow"></div>
    <div class="circle green" color="green"></div>
    </div>`;
  }
}
const ShowAndereLichten = function(data){
  console.log(data.status.verkeerslichtid);
  if(data.status.verkeerslichtid == 1){
    html_lichten3.innerHTML = `<div class="lichten">
    <div class="circle red" color="red"></div>
    <div class="circle" color="yellow"></div>
    <div class="circle" color="green"></div>
    </div>`;
  }
  else if(data.status.verkeerslichtid == 2){
    html_lichten3.innerHTML = `<div class="lichten">
    <div class="circle" color="red"></div>
    <div class="circle yellow" color="yellow"></div>
    <div class="circle" color="green"></div>
    </div>`;
  }
  else{
    html_lichten3.innerHTML = `<div class="lichten">
    <div class="circle" color="red"></div>
    <div class="circle" color="yellow"></div>
    <div class="circle green" color="green"></div>
    </div>`;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  html_lichten = document.querySelector(".lichten1");
  html_lichten2 = document.querySelector(".lichten2");
  html_lichten3 = document.querySelector(".lichten3");
  listenToUI();
  getLichten(1);
  getAndereLichten(2);
  listenToSocket();
});
