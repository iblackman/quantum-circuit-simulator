

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}
//drop modificado para criar uma copia do objeto que foi arrastado
function dropCopy(ev) {
    ev.preventDefault();
    //variavel de controle para voltar ao estado inicial
    var reset = false;
    //armazena valor anterior para caso seja cancelada a acao
    var prevValue = $(ev.currentTarget).find("img").attr("value");
    var preNodeCopy = $(ev.currentTarget).find("img").clone();
    //limpa div
    ev.currentTarget.innerHTML = '';

    var data = ev.dataTransfer.getData("text");
    var nodeCopy = document.getElementById(data).cloneNode(true);

    nodeCopy.id = "newId"; /* We cannot use the same ID */
    nodeCopy.setAttribute('draggable', false);
    ev.currentTarget.appendChild(nodeCopy);

    var nodeCopyValue = $(nodeCopy).attr("value");

    if(nodeCopyValue == "not" || nodeCopyValue == "sw") {
        var col = $(ev.currentTarget).attr("value");
        var lin1 = $(ev.currentTarget).parent().index();
        var lin2 = waitForClick();
        var pos1 = $(ev.currentTarget).position();
        
        if(lin1 == lin2) {
            reset = true
        } else {
            var pos2 = $(getCircuitElement(lin2, col)).position();
            //desenha linha
            connect($(ev.currentTarget), getCircuitElement(lin2, col), "black", 1);
            placePoint(lin2, col);
        }
    }

    if(reset){
        ev.currentTarget.innerHTML = '';
        ev.currentTarget.appendChild(preNodeCopy);
    }
}
//adiciona um novo circuito, que 'e apenas uma copia do circuito original
function duplicate() {
    var original = document.getElementById('container-original');
    var clone = original.cloneNode(true);

    //para aumentar o tamanho da div para mostrar o novo circuito
    increaseContainer($('.c-container-original').outerHeight());

    var divCircuitos = document.getElementById('circuitos');
    var index = divCircuitos.childElementCount - 1;
    clone.id = 'container' + index;
    clone.className = 'c-container';
    divCircuitos.appendChild(clone);
}
//remove circuito onde houve o click
function remove(ev) {
    ev.preventDefault();

    //diminui o tamanho da div
    decreaseContainer($('.c-container-original').outerHeight());
    //exclui circuito
    ev.currentTarget.parentElement.remove();
}
//aumenta a altura do container dos circuitos
function increaseContainer(h) {
    $('.container-outer').height($('.container-outer').height() + h);
}
//diminui a altura do container dos circuitos
function decreaseContainer(h) {
    $('.container-outer').height($('.container-outer').height() - h);
}
//ajusta tamanho da div dependendo do numero de max portas no circuito
function adjustCircuitWidth() {
    $("#circuitos").width($("#container-original").outerWidth());
}
//para capturar o click no proximo elemento
function waitForClick() {
    return 2;
}
//retorna o elemento do circuito utilizando os paramentros de ciruito (lin) e porta (col)
function getCircuitElement(lin, col){
    return $($("#circuitos").children().get(lin)).children().get(col);
}
function placePoint(lin, col) {
    var original = document.getElementById('dragpoint');
    var clone = original.cloneNode(true);
    var dest = $($("#circuitos").children().get(lin)).children().get(col);

    dest.innerHTML = '';

    clone.id = "newId"; /* We cannot use the same ID */
    clone.setAttribute('draggable', false);
    dest.append(clone);
}
//http://stackoverflow.com/questions/8672369/how-to-draw-a-line-between-two-divs
function getOffset( el ) {
    return {
        left: $(el).position().left,
        top: $(el).position().top,
        width: $(el).width(),
        height: $(el).height()
    };
}
function connect(div1, div2, color, thickness) { // draw a line connecting elements
    var off1 = getOffset(div1);
    var off2 = getOffset(div2);
    // bottom right
    var x1 = off1.left + off1.width/2;
    var y1 = off1.top + off1.height/2;
    // top right
    var x2 = off2.left + off2.width/2;
    var y2 = off2.top + off2.height/2;
    // distance
    var length = Math.sqrt(((x2-x1) * (x2-x1)) + ((y2-y1) * (y2-y1)));
    // center
    var cx = ((x1 + x2) / 2) - (length / 2) + 2; // +2 para corrigir erro da imagem
    var cy = ((y1 + y2) / 2) - (thickness / 2);
    // angle
    var angle = Math.atan2((y1-y2),(x1-x2))*(180/Math.PI);
    // make hr
    var htmlLine = "<div style='padding:0px; margin:0px; height:" + thickness + "px; background-color:" + color + "; line-height:1px; position:absolute; left:" + cx + "px; top:" + cy + "px; width:" + length + "px; -moz-transform:rotate(" + angle + "deg); -webkit-transform:rotate(" + angle + "deg); -o-transform:rotate(" + angle + "deg); -ms-transform:rotate(" + angle + "deg); transform:rotate(" + angle + "deg);' />";
    //
    // alert(htmlLine);
    document.body.innerHTML += htmlLine;
}
