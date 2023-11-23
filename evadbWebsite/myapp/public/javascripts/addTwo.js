const ip = "http://54.147.77.174"
// const ip = "http://localhost:3000"


function addTwoNumbers(p1, p2) {
  return parseInt(p1) + parseInt(p2);
}

function createNewElement(summationData, client) {
  sumTwo = document.createElement("p")
  if (client == true) {
    sumTwo.innerHTML = "Sum of input calculated on client is " + summationData
  }
  else {
    sumTwo.innerHTML = "Sum calculated on server is " + summationData
  }
  document.body.appendChild(sumTwo)
}

window.onload = function () {
  // document.getElementById("submitButton").addEventListener("click", function () {
  //   firstNumber = document.getElementById("firstNum");
  //   // console.log(firstNumber.value)
  //   secondNumber = document.getElementById("secondNum");
  //   var solution = addTwoNumbers(firstNumber.value, secondNumber.value);
  //   createNewElement(solution, true)
  // });

  // // client makes a post request
  // document.getElementById("serverSubmit").addEventListener("click", function(){
  //   firstNumber = document.getElementById("firstNum");
  //   // console.log(firstNumber.value)
  //   secondNumber = document.getElementById("secondNum");
  //   const data = {"first": firstNumber.value, "second": secondNumber.value, "javascript": true}
  //   console.log(data);

  //   fetch(ip, {
  //     method: 'POST',
  //     headers: {'Content-Type': 'application/json'},
  //     body: JSON.stringify(data)
  //   }).then((x)=>x.json())
  //   .then((data)=>createNewElement(data.result, false))
  // });


  // document.getElementById("pythonSubmit").addEventListener("click", function(){
  //   firstNumber = document.getElementById("firstNum");
  //   // console.log(firstNumber.value)
  //   secondNumber = document.getElementById("secondNum");
  //   const data = {"first": firstNumber.value, "second": secondNumber.value, "javascript": false}
  //   console.log(data);
  //   const pythonip = ip.concat("python")
  //   console.log(pythonip)
  //   fetch(pythonip, {
  //     method: 'POST',
  //     headers: {'Content-Type': 'application/json'},
  //     body: JSON.stringify(data)
  //   }).then((x)=>x.json())
  //   .then((data)=>createNewElement(data.result, false))
  // });


  function displayImage(path) {
    var img = document.createElement('img');
    img.src = path;
    img.width = "225";
    img.height = "225";
    document.getElementById("sudo").appendChild(img);
  }

  document.getElementById("Swap").addEventListener("click", function (event) {
    event.preventDefault()
    var form = document.getElementById("form");
    var formData = new FormData(form);
    console.log(formData)
    fetch(ip + "/Swap", {
      method: 'POST',
      body: formData,
    }).then(function (x) {
      return x.json()
    })
      .then((data) => displayImage(data.op_path));
  })
}
