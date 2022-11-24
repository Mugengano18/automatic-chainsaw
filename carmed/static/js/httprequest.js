let city_field = document.getElementById("inputCity");
let district_field = document.getElementById("inputDistrict")
let sector_field = document.getElementById("inputSector");
let cell_field = document.getElementById("inputCell");
var pair=[];

console.log(city_field)
const options = {
  method: "GET",
  headers: {
    "X-RapidAPI-Key": "3a85e2a9femshc75f599f0f8d052p1cdebajsn8b711f561255",
    "X-RapidAPI-Host": "rwanda.p.rapidapi.com",
  },
};

fetch("https://rwanda.p.rapidapi.com/provinces", options)
  .then((response) => response.json())
  .then((response) => {
    let data_all = response.data;
    for (var province in data_all) {
      pair = data_all[province];
      console.log(pair)
      city_field.innerHTML += `<option value = "${pair}">${pair}</option>`
    }
  })
  .catch((err) => console.error(err));




function populate(s1, s2) {
  district_field.innerHTML="";
  var s1 = document.getElementById(s1);
  var s2 = document.getElementById(s2);

  s2.innerHtML = "";


  fetch(`https://rwanda.p.rapidapi.com/districts?p=${s1.value}`, options)
  .then((response) => response.json())
  .then((response) => {
    let data_all = response.data;
    console.log(data_all)
    for (var province in data_all) {
      pair = data_all[province];
      district_field.innerHTML += `<option value = "${pair}">${pair}</option>`
    }
  })
  .catch((err) => console.error(err));
  
}

function populateSector(province,district) {
  sector_field.innerHTML="";
  
  var s1 = document.getElementById(province);
  var s2 = document.getElementById(district);
  

  s2.innerHtML = "";


  fetch(`https://rwanda.p.rapidapi.com/sectors?p=${s1.value}&d=${s2.value}`, options)
  .then((response) => response.json())
  .then((response) => {
    let data_all = response.data;
    console.log(data_all)
    for (var province in data_all) {
      pair = data_all[province];
      console.log(pair)
      inputSector.innerHTML += `<option value = "${pair}">${pair}</option>`
    }
  })
  .catch((err) => console.error(err));
  
}
