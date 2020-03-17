//<script id="Изменение ДФН по выбранному селекту">
function Change_dfn(ind) {
    // получаем индекс выбранного элемента
    var selind = document.getElementById(ind).options.selectedIndex;
    var txt = document.getElementById(ind).options[selind].text;
    //var val= document.getElementById("16").options[selind].value;
    var elem = ind + "_"
    var tag = document.getElementById(elem)
    alert(tag.getAttribute("def"));
    tag.setAttribute("def", txt);
    //tag.setAttribute("data-about", txt);
    alert(tag.getAttribute("def"));
}

    //document.getElementById("16").addEventListener("change", Change_dfn);
//</script>

<!--<script id="Message under <elem id='coords-show-mark'">
let elem = document.getElementById("okno");

function createMessageUnder(elem, html) {
  // создаём элемент, который будет содержать сообщение
  let message = document.createElement('div');
  // для стилей лучше было бы использовать css-класс здесь
  message.style.cssText = "position:fixed; color: red";

  // устанавливаем координаты элементу, не забываем про "px"!
  let coords = elem.getBoundingClientRect();

  message.style.left = coords.left + "px";
  message.style.top = coords.bottom + "px";

  message.innerHTML = html;

  return message;
}
let message = createMessageUnder(elem, 'Hello, world!');
document.body.append(message);
setTimeout(() => message.remove(), 5000);
</script > -->

  
  //Чтение локального файла средствами JavaScript
  function readFile(object) {
    var file = object.files[0]
    var reader = new FileReader()
    reader.onload = function () {
      document.getElementById('out').innerHTML = reader.result
    }
    reader.readAsText(file)
  }
  //html
  < input type = "file" id = "file" >
    <button onclick="readFile(document.getElementById('file'))">Read!</button>
    <div id="out"></div>