$(function(){

	var internel;
	localStorage.setItem("dyna", "none");

	$(".dynamicinfo").click(function(){
		var dyna = localStorage.getItem("dyna");
		if (dyna == "done")
		{
			// 已经扫描过了，什么都不用修改
		}
		else{
			var filename = localStorage.getItem("realName");
			// if( (filename.indexOf(".exe") > 0) || (filename.indexOf(".EXE") > 0))
			// {
				// 扫描前清除原来的DOM元素
				$(".dynamic").remove();
				localStorage.setItem("dyna", "done");
				var filename = localStorage.getItem("filename");
				isScaning();
				internel = setInterval(function(){getresult(filename);}, 1000);
			// }
			// else{
			// 	// alert("只能动态分析可执行文件！");
			// 	$('#filterfile').modal('show');
			// }
		}
	});

	function getresult(filename){
		$.ajax({
			type:"POST",
			url:"",
			data:{filename:filename},
			success: function (msg)
			{
				var result = eval("("+msg+")");

				if (result['isexe'] == 0) {
					$('#filterfile').modal('show');
					// 清除定时器
					clearInterval(internel);
					backnormal();
				}

				if(result['ischeck'] == 2)
				{
					if (result['result'] == 0) {
						$("#tab3").append("<div class='dynamic'></div>");
						$(".dynamic").html("未发现异常");
					}
					else{
						var res;
						var row;

						// 返回显示状态
						result['result'] = result['result'].replace(/\|/g,"\\");
						result['result'] = result['result'].replace(/Create:/g,"创建文件&nbsp;&nbsp;&nbsp;");
						res = result['result'].split("\n");
						$("#tab3").append("<div class='dynamic'></div>");

						res.forEach(function(x){
							row = "<div class='changerow'>"+ x +"</div>";
							$(".dynamic").append(row);
						});
					}
					
					// 清除定时器
					clearInterval(internel);

					backnormal();
				}
			}	
		});
	}

	// 扫描模式
	function isScaning(){
		// 设置扫描gif
		$(".gif > img").attr("src","img/scan.gif");
		// 换上绿框
		$(".analyzeShow").css("display","block");
	}

	// 返回常态
	function backnormal(){
		// 撤销绿框
		$(".analyzeShow").css("display","none");
		// 替换扫描图片
		$(".gif > img").attr("src","img/scanstatic.png");
	}
})