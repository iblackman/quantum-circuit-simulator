

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

    var col = getElemntCol(ev.currentTarget);
    var lin1 = getElementLin(ev.currentTarget);
    //caso tenha q ligar
    if(nodeCopyValue == "not" || nodeCopyValue == "sw") {
        var lin2 = getCircuitToLink();
        var pos1 = $(ev.currentTarget).position();
        
        if(lin1 == lin2) {
            reset = true
            alert("Porta arrastada para o mesmo circuito da conexao, por favor mude um dos dois.");
        } else {
            var pos2 = $(getCircuitElement(lin2, col)).position();
            //desenha linha
            var valConex = lin1+"-"+lin2+"-"+col;
            connect($(ev.currentTarget), getCircuitElement(lin2, col), "black", 1, valConex);
            placePoint(lin2, col);
        }
    }
    //caso tentou ligar com a mesma linha do circuito cancela
    if(reset){
        ev.currentTarget.innerHTML = '';
        ev.currentTarget.appendChild(preNodeCopy[0]);
    }

    //se a antiga porta era uma de bit duplo deve limpar sua conexao
    if(prevValue == "not" || prevValue == "sw"){
    	console.log("tem q apagar conexao e ponto");
    	limparConexao(lin1, col, 0);
    }else if(prevValue == "point"){
    	console.log("tem q apagar conexao e porta");
    	limparConexao(lin1, col, 1);
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
    //ajusta numeracao
    renumeraCircuitos();
}
//remove circuito onde houve o click
function remove(ev) {
    ev.preventDefault();
    //limpa todos as portas do circuito, para cancelar as conexoes
    resetarCircuito(ev.currentTarget);
    //diminui o tamanho da div
    decreaseContainer($('.c-container-original').outerHeight());
    //exclui circuito
    ev.currentTarget.parentElement.remove();
    //ajusta numeracao
    renumeraCircuitos();
}
//reseta circuito, tudo line
function resetarCircuito(elem){
	var circuit = $(elem.parentElement);
	var len = $(circuit).children(".c-porta").length;
	var lin = $(circuit).index();
	$(circuit).find(".c-porta").each(function(){
		var porta = $(this).find("img").attr("value");
		var col = $(this).attr("value");
		//console.log(col+" - "+lin+" - "+porta);
		//limpa conexao dos elementos
		if(porta == "not" || porta == "sw"){
	    	//console.log("tem q apagar conexao e ponto");
	    	limparConexao(lin, col, 0);
	    }else if(porta == "point"){
	    	//console.log("tem q apagar conexao e porta");
	    	limparConexao(lin, col, 1);
	    }
	});
	
	console.log(len);
}
//a partir da col e linha deleta a conexao e o ponto ou a porta
function limparConexao(lin, col, type){
	$('.conexao-circuito').each(function(){
		var str = $(this).attr('value');
		var strArray = str.split('-');
		if(type){//substituiram o ponto, tenho que apagar a porta
			if(strArray[1] == lin && strArray[2] == col){
				placeLine(strArray[0],col);
				$(this).remove();
			}
		}else{//substituiram a porta, tenho que apagar o ponto
			if(strArray[0] == lin && strArray[2] == col){
				placeLine(strArray[1],col);
				$(this).remove();
			}
		}
	});
}
//refaz a numeracao dos circuitos
function renumeraCircuitos(){
	$("#circuitos .c-container").each(function(index){
		$(this).find("span").html(index + 1);
	});
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
//retorna o circuito a ser linkado em funcao do valor do input
function getCircuitToLink() {
	var circ = $("#link-to-circuit").val();
	//checa se existe a linha, caso contrario pega a mais proxima
	var count = $("#circuitos").children().length - 1;
	if(circ < 1){
		circ = 1;
	}else if(circ > count){
		circ = count;
	}
    return circ;
}
//retorna o elemento do circuito utilizando os paramentros de ciruito (lin) e porta (col)
function getCircuitElement(lin, col){
    return $($("#circuitos").children().get(lin)).children("div").get(col);
}
//retorna a coluna do elemento droppable passado
function getElemntCol(elem){
	return $(elem).attr("value");
}
//retorna a linha do elemento droppable passado
function getElementLin(elem){
	return $(elem).parent().index();
}
//coloca o ponto em funcao da linha e coluna passadas
function placePoint(lin, col) {
    placePorta(lin,col,'dragpoint');
}
//coloca o linha em funcao da linha e coluna passadas
function placeLine(lin, col) {
    placePorta(lin,col,'dragline');
}
//coloca a porta passada em funcao da linha e coluna
function placePorta(lin,col,porta){
	var original = document.getElementById(porta);
    var clone = original.cloneNode(true);
    var dest = $($("#circuitos").children().get(lin)).children("div").get(col);

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
function connect(div1, div2, color, thickness, valConex) { // draw a line connecting elements
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
    var htmlLine = "<div class='conexao-circuito' value='"+valConex+"' style='padding:0px; margin:0px; height:" + thickness + "px; background-color:" + color + "; line-height:1px; position:absolute; left:" + cx + "px; top:" + cy + "px; width:" + length + "px; -moz-transform:rotate(" + angle + "deg); -webkit-transform:rotate(" + angle + "deg); -o-transform:rotate(" + angle + "deg); -ms-transform:rotate(" + angle + "deg); transform:rotate(" + angle + "deg);' />";
    //
    // alert(htmlLine);
    document.body.innerHTML += htmlLine;
}

//calcular o circuito
function calcular(){
	var data = [];
	var msg = "";
	var len = $("#circuitos .c-container").length;
	if(len > 0){
		// Monta array dos circuitos
		data = getCircuitos();
		// cacula tempo de execucao com base nos inputs
		var dataTempo = calculaTempo();
		var strTempo = printTempo(dataTempo.data);

		console.log(data);
		console.log(data[0]);
		$.ajax({
			url: 'ajax/calcular/',
			data: JSON.stringify({
				'data' : data,
				'len' : len
			}),
			type: 'POST',
			dataType: 'json',
			success: function(response){
				console.log("Success");
				var tes = response.msg;
				console.log(tes);
				msg = tes;
				console.log(response);
				var resultTxt = printResult(response.result);
				$('.resultado-circuito').html(response.msg + "<br/><br/>"+ strTempo +"Tempo maximo estimado: " + dataTempo.maxTempo + "ms" + "<br/><br/>"+ 
					resultTxt );
			},
			fail: function(response){
				console.log("Fail");
			}
		});
	}else{
		msg = "Crie ao menos um circuito e clique em Calcular"
		$('.resultado-circuito').html(msg);
	}
}
//retorna um array com cada circuito, onde cada circuito 'e um array com as portas daquele circuito'
function getCircuitos(){
	var data = new Object();
	$("#circuitos .c-container").each(function(index){
		var circuito = [];
		var stCircuit = "";
		var value;
		$(this).find(".c-porta").each(function(){
			value = $(this).find("img").attr('value');
			circuito.push(value);
			stCircuit += value + ",";
			value = null;
		});
		data[index] = circuito;
	});
	return data;
}
//Retorna um array map com os tempos das portas
//key => value porta
//value => tempo no input
function getPortaTempos(){
	var tempos = new Object();
	$("div.porta-tempo input").each(function(index){
		var alt = $(this).attr("alt");
		var porta = alt.split(" ")[1];
		var value = parseInt($(this).val());
		tempos[porta] = value;
	});
	return tempos;
}
//calcula o maior tempo dentre todos os circuitos
//tambem quis aproveitar para montar uma estrutura com os tempos para facilitar a alteracao dele quando existe dependencia (porta 2-bits, onde um tem q esperar o outro)
function calculaTempo(){
	var tempos = getPortaTempos();
	var maxTempo = 0;
	var arrTempos = new Array();
	//itera entre os circuitos
	$("#circuitos .c-container").each(function(index){
		var cTempo = 0;
		//calcula o tempo total do circuito
		arrTempos[index] = [];
		$(this).find(".c-porta").each(function(){
			var value = $(this).find("img").attr('value');
			//tempo da porta
			var pTempo = tempos[value];
			cTempo += pTempo;
			arrTempos[index].push(cTempo);
		});
		//armazena valor maximo
		if (cTempo > maxTempo){
			maxTempo = cTempo;
		}
	});
	res = {"maxTempo" : maxTempo,
			"data" : arrTempos};
	return res;
}
//gera a string do array de tempo passado
function printTempo(data){
	var res = "";
	for (var i = 0; i < data.length; i++){
		for (var j = 0; j < data[i].length; j++){
			res += " => " + data[i][j];
		}
		res += "<br/>";
	}
	return res;
}

//gera string de resposta do resultado
function printResult(data){
	var res = "";
	for (var i = 0; i < data.length; i++){
		res += (i+1)+" -> [";
		for (var j = 0; j < data[i].length; j++) {
			if (j != 0){
				res += ", ";
			}
			res += roundUp(data[i][j], 10000);
		}
		res += "]<br/>";
	}
	return res;
}

//arrendodar numero
function roundUp(num, precision) {
  return Math.ceil(num * precision) / precision
}