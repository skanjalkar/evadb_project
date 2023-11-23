var express = require('express');
var fs = require('fs');
var router = express.Router();
const path = require('path');
var process = require('process');
const multer = require('multer');
const storage = multer.diskStorage({
  destination: function(req, file, cb){
    cb(null, './public/images/awsImages/')
  },
  filename: function(req, file, cb){
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random()*1E9)
    cb(null, file.fieldname + "-" + uniqueSuffix + ".jpg")
  }
});

const upload = multer({storage: storage});

const images = upload.fields([{
  name:'image1'
},
{
  name:'image2'
}]);

router.post('/Swap', images, function(req, res, next){
  const spawn = require("child_process").spawn;
  var path1 = req.files.image1[0].path;
  var path2 = req.files.image2[0].path;
  var original_name1 = req.files.image1[0].originalname
  var original_name2 = req.files.image2[0].originalname
  const pyProcess = spawn('python3', ["/home/ubuntu/awsFaceSwap/Wrapper.py", path1, path2, original_name1, original_name2])
  pyProcess.stdout.on('data', (data)=>{
    var path = {
      "op_path": data.toString('utf-8')
    }
    res.json(path);
    console.log("Swapped image!")
  })
  console.log("Started swapping...")
  // console.log("Sent original image")
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express', today: 'Shreyas' });
});

router.get('/starter', function(req, res, next){
  res.render('starter');
})

router.post('/', function(req, res, next){
  var info = req.body;
  var summation = parseInt(info.first) + parseInt(info.second);
  var data = {
    "result": summation
  };
  res.json(data)
  console.log("Success")
});

router.post('/python', function(req, res, next){
  var info = req.body
  const spawn = require("child_process").spawn;
  console.log('Current directory' + process.cwd());
  console.log(__dirname);
  console.log(fs.existsSync("./../pythonscripts/addtwo.py"));
  // const pythonProcess = spawn('ls');
  const pythonProcess = spawn('python3', ["./../pythonscripts/addtwo.py", parseInt(info.first), parseInt(info.second)]);
  pythonProcess.stderr.on('error', function(error){
    console.log("error")
    var err = {
      "error": "Something went wrong"
    }
    res.json(err)
  })
  pythonProcess.stdout.on('data', (data)=>{
    console.log(data)
    console.log(data.toString('utf-8')); // value is a string, result and \n <Buffer 32 0a>
    var summation = {
      "result": data.toString('utf-8')
    };
    res.json(summation);

    console.log("Success");
  });
});

module.exports = router;
