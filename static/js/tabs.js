$(function(){
	$("ul li:first a").attr('id','current');
	$("#tabContent > div").hide();
	$("#tabContent > div:first").fadeIn();
	
	function resetTabs()
	{
		// 如果只是把其他的隐藏了，那么最后只会显示最后一个点击的选项卡
		$("#tabContent > div").hide();
		// 所以需要把其他所有的a的id给清空
		$("#tabs li").attr("id","other");
	}

	$("li").click(function(){
		if ($(this).attr("id") == "current") {
			return;
		}
		else {
			// 如果不清除之前的样式，会造成多个选项卡都堆积在一起
			resetTabs();
			$(this).attr("id", "current");
			$($(this).children("a").attr("name")).fadeIn();
		}
		
	});

	$("tr:odd").css("background","white");
});