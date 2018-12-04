// https://gist.github.com/shiawuen/1534477

function slice_and_send(f, url, new_url, framelength) {

var framesize = 1024768;

var written_frame = 0;

if (f.files.length)
  processFile();

function processFile(e) {
  var file = f.files[0];
  var size = file.size;
  var sliceSize = framesize;
  var start = 0;

  setTimeout(loop, 1);

  function loop() {
    var end = start + sliceSize;
    
    if (size - end < 0) {
      end = size;
    }
    
    var s = slice(file, start, end);

    send(s, start, end, url, new_url);

    if (end < size) {
      start += sliceSize;
      setTimeout(loop, 100);
    }
  }
}


function send(piece, start, end, url, new_url) {
  var formdata = new FormData();
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() { // 요청에 대한 콜백
  if (xhr.readyState === xhr.DONE) { // 요청이 완료되면
    if (xhr.status === 200 || xhr.status === 201) {
      progress();
    } else {
      noop();
    }
  }
  };

  xhr.open('POST', url, true);

  formdata.append('start', start);
  formdata.append('end', end);
  formdata.append('key', new_url)
  formdata.append('file', piece);

  xhr.send(formdata);
}

/**
 * Formalize file.slice
 */

function slice(file, start, end) {
  var slice = file.mozSlice ? file.mozSlice :
              file.webkitSlice ? file.webkitSlice :
              file.slice ? file.slice : noop;
  
  return slice.bind(file)(start, end);
}

function noop() {
  $('#done').html("Failed for some reason :( please try again!");
}

function progress() {
  written_frame = written_frame + 1;
  percent = written_frame / framelength * 100;

  console.debug(written_frame + ' / ' + framelength);
  $('#done').html(percent.toFixed(2) + "% completed");

  if(written_frame == framelength) setTimeout(done, 2500);
}

function done() {
  var s = location.protocol + '//' + location.hostname + ':' + location.port + '/get/' + new_url;
  $('#done').html("SUCCESS and FILE URL IS " + "<a href = \"" + s + "\">" + s + "</a>");

}

}