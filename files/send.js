// https://gist.github.com/shiawuen/1534477

function slice_and_send(f, url, new_url) {

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

    send(s, start, end, url);

    if (end < size) {
      start += sliceSize;
      setTimeout(loop, 1);
    }
  }
}


function send(piece, start, end, url, new_url) {
  var formdata = new FormData();
  var xhr = new XMLHttpRequest();

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
  
}

}