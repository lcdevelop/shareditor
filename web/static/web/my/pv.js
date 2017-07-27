// 为了过滤爬虫，上报的信息是通过js渲染进行的，同时渲染出来的是个图片，这样可以过滤大部分爬虫
$(function()
{
    var gif_url = '/report/pv.gif?url=' + window.location.href;
	var report ="<img id='report_gif' src='" + gif_url + "'>";
	$("#report").html(report);
    $("#report").css('height', 0);
    $("#report").css('width', 0);
});