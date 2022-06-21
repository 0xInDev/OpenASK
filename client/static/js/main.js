var datas = {};
var elements = [];
var currentElement = 0;

// template for field
var checkSamples = `
	<label class="form-check-label">
	  <input class="form-check-input checkbox" type="checkbox" id="check#question_id#proposal_id" onclick="valueChange(#question_id,#proposal_id)">
	  <span>
	  #value
	  </span>
	</label>
	`;
var radioSamples = `
	<label class="form-radio-label">
	  <input class="form-radio-input" type="radio" name="radio#question_id" id="radio#question_id#proposal_id" onclick="radioValueChange(#question_id,#proposal_id)" option="#proposal_id">
	  <span>#value</span>
	</label>
	`;
var textSamples = `
	<div>
	  <input class="text_input" type="text" name="text#question_id" id="text#question_id" onchange="textValueChange(#question_id)" placeholder="text..." onkeypress="textValueChange(#question_id)">
	</div>
	`;
var numberSamples = `
	<div>
	  <input class="text_input" type="number" onkeydown="return isNumberKey(event)" name="number#question_id"  id="number#question_id"  placeholder="123..." onchange="numberValueChange(#question_id)" onkeypress="numberValueChange(#question_id)">
	</div>
	`;

// Function for detecting field change
function valueChange(question_id, proposal_id) {
	if (datas[question_id].indexOf(proposal_id) !== -1) {
		datas[question_id] = datas[question_id].filter(function (e) {
			return e !== proposal_id;
		});
	} else {
		datas[question_id].push(proposal_id);
	}
}

function isNumberKey(evt) {
	var charCode = event.key;
	number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Backspace"];

	if (evt.target.value.length > 15 && charCode != "Backspace") {
		return false;
	}

	if (number.includes(charCode)) return true;
	else {
		return false;
	}
}

function radioValueChange(question_id, proposal_id) {
	let widget = $("#radio" + question_id + "" + proposal_id);
	datas[question_id] = proposal_id;
}

function textValueChange(question_id) {
	datas[question_id] = $("#text" + question_id).val();
}

function numberValueChange(question_id) {
	if (!parseInt($("#number" + question_id).val())) {
		$("#number" + question_id).val;
	}
	datas[question_id] = parseInt($("#number" + question_id).val());
}

// Function for add new field
function addCheckBox(e) {
	let cs = "";
	e.response_proposal.forEach(function (v) {
		let sCheck = checkSamples
			.replaceAll("#question_id", e.id)
			.replaceAll("#proposal_id", v.id)
			.replaceAll("#value", v.libelle);
		cs = cs + "" + sCheck;
	});
	$("#questionBox").append(
		'<div style="display: None" id="quest_' +
			e.id +
			'"><h3>' +
			e.libelle +
			"</h3><br>" +
			cs +
			"</div>"
	);
	elements.push("quest_" + e.id);
}

function addRadio(e) {
	let cs = "";
	e.response_proposal.forEach(function (v) {
		let sCheck = radioSamples
			.replaceAll("#question_id", e.id)
			.replaceAll("#proposal_id", v.id)
			.replaceAll("#value", v.libelle);
		cs = cs + "" + sCheck;
	});
	$("#questionBox").append(
		'<div style="display: None" id="quest_' +
			e.id +
			'"><h3>' +
			e.libelle +
			"</h3><br>" +
			cs +
			"</div>"
	);
	elements.push("quest_" + e.id);
}

function addText(e) {
	let sText = textSamples.replaceAll("#question_id", e.id);
	$("#questionBox").append(
		'<div style="display: None" id="quest_' +
			e.id +
			'"><h3>' +
			e.libelle +
			"</h3><br>" +
			sText +
			"</div>"
	);
	elements.push("quest_" + e.id);
}
function addNumber(e) {
	let sNumber = numberSamples.replaceAll("#question_id", e.id);
	$("#questionBox").append(
		'<div style="display: None" id="quest_' +
			e.id +
			'"><h3>' +
			e.libelle +
			"</h3><br>" +
			sNumber +
			"</div>"
	);
	elements.push("quest_" + e.id);
}

// Question navigation

function next() {
	$("#" + elements[currentElement]).css("display", "None");
	currentElement = currentElement + 1;
	console.log("#" + elements[currentElement]);
	$("#" + elements[currentElement]).css("display", "block");
	console.log(elements.length, currentElement);
	if (currentElement == elements.length - 1) {
		$("#next").css("display", "none");
		$("#validate").css("display", "block");
	} else {
		$("#next").css("display", "block");
		$("#validate").css("display", "none");
	}

	if (currentElement > 0 && currentElement < elements.length) {
		$("#prev").css("visibility", "visible");
	} else {
		$("#prev").css("visibility", "hidden");
	}
}

function prev() {
	$("#" + elements[currentElement]).css("display", "None");
	currentElement = currentElement - 1;
	$("#" + elements[currentElement]).css("display", "block");
	$("#validate").css("display", "none");
	if (currentElement == elements.length - 1) {
		$("#next").css("display", "none");
	} else {
		$("#next").css("display", "block");
	}

	if (currentElement > 0 && currentElement < elements.length - 1) {
		$("#prev").css("visibility", "visible");
	} else {
		$("#prev").css("visibility", "hidden");
	}
}

// When user want to submit sondage
function validate() {
	let data = {
		person: { email: $("#email").val() },
		sondage: sondage,
		responses: datas,
	};
	console.log(data);
	$.ajax({
		type: "POST",
		url: "/response/submit/",
		dataType: "json",
		contentType: "application/json",
		async: false,
		data: JSON.stringify(data),
		success: function (rs) {
			if ("status" in rs) {
				$("#questionBox").html("");
				$("#ok").toggleClass("d-none");
				$("#ok").html(
					'<lottie-player src="https://assets2.lottiefiles.com/packages/lf20_unahkkgk.json"  background="transparent"  speed="1"  style="width: 240px; height: 240px;margin: auto;"   autoplay></lottie-player><p class="text-success mt-2 ">Formulaire envoyé</p>'
				);
				$("#boxBottom").toggleClass("d-none");
			} else {
				$("#alert").toggleClass("d-none");
				setTimeout(() => {
					$("#alert").toggleClass("d-none");
				}, 2000);
				console.log(rs);
			}
		},
	});
}

// Fetch sondage and create html element
$(document).ready(function () {
	if (sondage != null)
		$.get("/sondage/" + sondage + "/details/", function (result) {
			$("#sondageName").text(result.sondage.libelle);
			$("#sondageDescription").text(result.sondage.description);
			elements.push("quest_zero");
			elements.push("quest_0");
			result.sondage.questions.forEach(function (e) {
				if (e.type_response == 0) {
					datas[e.id] = null;
					addRadio(e);
				} else if (e.type_response == 1) {
					datas[e.id] = [];
					addCheckBox(e);
				} else if (e.type_response == 2) {
					datas[e.id] = "";
					addText(e);
				} else if (e.type_response == 3) {
					datas[e.id] = null;
					addNumber(e);
				}
			});
		});
});
