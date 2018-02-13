const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const archiver = require('archiver');
const request = require('request');

const app = express();

app.use(express.static('public'));
app.use(bodyParser.json());

app.post('/run', (req, res) => {
  console.log('Received code');
  console.log(req.body.code);

  fs.writeFile('data/files/main.py', req.body.code, err => {
    console.log('Written code');

    let fileOutput = fs.createWriteStream('./data/code.zip');
    fileOutput.on('close', () => {
      console.log('Written archive');

      let formData = {
        uploaded_file: fs.createReadStream('./data/code.zip')
      };
      request.post({
        url: 'http://robot.sr/upload/upload',
        formData: formData
      }, (err, httpResponse, body) => {
        if(err) throw err;        
        console.log('Uploaded archive');

        formData = {
          zone: "0",
          mode: "development"
        };
        request.post({
          url: 'http://robot.sr/run/start',
          formData: formData
        }, (err, httpResponse, body) => {
          if(err) throw err;
          console.log('Ran program');

          res.send();
        });
      });
    });

    let archive = archiver('zip');
    archive.pipe(fileOutput);
    archive.directory('data/files/', false);
    archive.on('error', err => { throw err; });
    archive.finalize();
  });
});

app.listen(8080, () => console.log('Server listening on port 8080!'));