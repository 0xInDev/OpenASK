// SiJs non minified source

class Router{

	sijs = undefined
	routes = []

	route(path) {
		this.routes.push(path)
		this.sijs.query(path,function(content){
			$("sibody").first().html(content)
		})
	}

	changeContent(path, elementId) {
		this.routes.push(path)
		this.sijs.query(path, function(content){
			$("#"+elementId).html(content)
		})
	}

	reload() {
		this.sijs.query(this.routes[this.routes.length-1],function(content){
			$("sibody").first().html(content)
		})
	}

	back() {
		this.routes.pop();
		this.reload()
	}
}

class SweetAlert{

	show(data,confirm=false,callback) {
		if(confirm==true) {
			Swal.fire(data).then((result) => {
				callback(result)
			}) 
		} else {
			Swal.fire(data)
		}
	}

	swal() {
		return Swal
	}

}

class Util{

	getDelimitter(text,delimitter) {
		text = text.split("{{")
		text.shift()
		var arr = []
		text.forEach(function(item) {
			item = item.split("}}")
			arr.push(item[0])
		})
		return arr;
	}
}

class ModalLoader {
 
	sijs = undefined

	getModal(path,id){
		this.sijs.query(path,function(content){
			$("simodal").first().html(content)
			$("#"+id).modal('toggle');
		})
		
	}

	removeModal(id) {
		$("#"+id).modal('hide')
		$(document).on('hidden', "#"+id, function () {
		    $(this).remove();
		});
	}

}
class Http {

	get(url, callback) {
        $.ajax({
            url: url,
            type: "GET",
            success: function (data) {
                callback(data)
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
	}
}
class SiJs extends Router {

	saved = []
	url = undefined
	util = undefined
	http = undefined

	constructor() {
		super().sijs = this
		this.util = new Util()
		var siJs = this
		this.http = new Http()
	}

	query(path, callback) {
		$.get(path,function(res) {
			callback(res);
			$('.loader-spinner').css('visibility','hidden')
		})
	}

	backQuery(path, callback) {
		$.get(path,function(res) {
			callback(res)
		})
	}

	modelize(data, name){
		var data = {"name":name, data:data}
		this.saved.push(data)
		this.updatePage()
	}

	getModel(name){
		var r = undefined
		this.saved.forEach(function(item){
			if(item['name']==name){
				r = item['data']
				return false
			}
		})
		return r
	}

	formValidator(formID, callback, errorCallback) {
		var forms = $("#"+formID+" input")
		var forms2 = $("#"+formID+" textarea")
		var error = false
		function changement(event){
			var target = $(event.target)
			if(target.val() != ""){
				target.css("border","1px solid forestgreen")
			} else{
			}
		}
		forms.each(function(index){
			var in_el = $(forms[index])
			
			if(in_el.attr('required')){
				if(in_el.val() == ""){
					in_el.css("border","1px solid red")
					in_el.change(changement)
					error = true
				}
			}
		})
		forms2.each(function(index){
			var in_el = $(forms2[index])
			
			if(in_el.attr('required')){
				if(in_el.val() == ""){
					in_el.css("border","1px solid red")
					in_el.change(changement)
					error = true
				}
			}
		})
		if(error == false){
			callback()
		} else {
			errorCallback()
		}
	}

	getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = cookies[i].trim();
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}

	loadModal(){
		this.modal = new ModalLoader()
		this.modal.sijs = this
	}

	loadSweetAlert(){
		this.sa = new SweetAlert()
	}

	loadCss(url) {
	    if (!$('link[href="' + url + '"]').length)
	        $('head').append('<link rel="stylesheet" type="text/css" href="' + url + '">');
	}

	updatePage(){
		let saved = this.saved
		$('[siloopmodel]').each(function(el){
			var ele = $($('[siloopmodel]')[el])
			var m = ele.attr('siloopmodel')
			var obj = ele.attr('loop')
			var u = new Util()
			for(var i = 0;i<saved.length;i++){
				var ii = saved[i]
				if(ii['name']==m){
					var datas = ii['data']
					datas.forEach(function(data){
						var c = ele.clone()
						var arg = u.getDelimitter(c.html(),"{{,}}")
						arg.forEach(function(e){
							var r = eval(e)
							c.html(c.html().replace("{{"+e+"}}",r))
						})
						ele.parent().append(c)
					})
					
					ele.remove()

				}
			}
		})
		$('[simodel]').each(function(el){
			var ele = $($('[simodel]')[el])
			var model = ele.attr('simodel')
			var varr = ele.attr('as')
			var u = new Util()
			for(var i = 0;i<saved.length;i++){
				var ii = saved[i]
				if(ii['name']==model){
					var datas = siJs.getModel(model)
					console.log(varr)
					eval('var '+varr+' = siJs.getModel(model)')
					var c = ele.clone()
					var arg = u.getDelimitter(c.html(),"{{,}}")
					arg.forEach(function(e){
						var r = eval(e)
						//console.log(r)
						c.html(c.html().replace("{{"+e+"}}",r))
					})
					ele.parent().append(c)
					ele.remove()
				}
			}
		})
	}
	update(){
		$("siinclude").each(function(index){
			var el = $($("siinclude")[index])
			var src = el.attr('src')
			siJs.include(src,el)
		})
	}
	include(path,element){
		this.query(path,function(content){
			element.html(content)
		})
	}
	preAjax(form, callback){
        $("#"+form+"").submit(function(e) {
        	$("#"+form).change(function() {
		        $("#"+form).valid()
		    });
		    if($("#"+form).valid()) {
		    	e.preventDefault();
	            var url = $("#"+form).attr('action')
	            var method = $("#"+form).attr('method')
	            var formData = new FormData(this);
	            $('.loader-spinner').css('visibility','visible')
	            $.ajax({
	                url: url,
	                type: method,
	                data: formData,
	                success: function (data) {
	                    callback(data)
	                },
	                cache: false,
	                contentType: false,
	                processData: false
	            });
	            e.stopImmediatePropagation();
	            return false;
		    } else {
		    	e.stopImmediatePropagation();
	            return false;
		    }
            
        });
    }
    wait(timer,callback){
    	setTimeout(callback, timer);
    }
    showToast(parameter) {
    	$('.jq-toast-wrap').removeClass('bottom-left bottom-right top-left top-right mid-center'); // to remove previous position class
	    $(".jq-toast-wrap").css({
	      "top": "",
	      "left": "",
	      "bottom": "",
	      "right": ""
	    }); //to remove previous position style
	    $.toast(parameter)
    }

}

const RESSOURCE_FETCH_METHOD = {
	ONLINE: 0,
	OFFLINE: 1,
	OFFLINEPROVIDERS: 2,
	ONLINEPROVIDERS: 3
}

var online_providers = {
	cloudflare: {
		js: "https://cdnjs.cloudflare.com/ajax/libs/<name>/<version>/<module_name>.js",
		css: "https://cdnjs.cloudflare.com/ajax/libs/<name>/<version>/<module_name>.css"
	}, 
	jsdelivr: {
		js: "https://cdn.jsdelivr.net/npm/<name>@<version>/dist/js/<module_name>.js",
		css: "https://cdn.jsdelivr.net/npm/<name>@<version>/dist/css/<module_name>.css"
	}
}