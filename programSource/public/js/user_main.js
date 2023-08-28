/*
	Introspect by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)

	Edited by June K. 2023/08/22
*/

// user_main.js
document.addEventListener("DOMContentLoaded", function() {
    const videoListContainer = document.getElementById("videoList");
    const originalNameList = document.getElementById("originalNameList");

    function fetchVideoData(selectedOriginalName) {
        // 서버에서 선택된 원본 이름에 해당하는 비디오 데이터를 가져옵니다.
        fetch(`/videos/${selectedOriginalName}`)
            .then(response => response.text())
            .then(html => {
                videoListContainer.innerHTML = html;
            })
            .catch(error => {
                console.error("비디오 데이터를 가져오는 중 오류 발생:", error);
            });
    }

	// 서버에서 originalName 목록을 가져와 드롭다운에 추가합니다.
    fetch("/original-names")
        .then(response => response.json())
        .then(data => {
            data.forEach(originalName => {
                const option = document.createElement("option");
                option.value = originalName;
                option.textContent = originalName;
                originalNameList.appendChild(option);
            });

            // 초기에 첫 번째 part1에 대한 비디오 데이터를 가져옵니다.
            if (data.length > 0) {
                fetchVideoData(data[0]);
            }
        })
        .catch(error => {
            console.error("originalName 목록을 가져오는 중 오류 발생:", error);
        });

	originalNameList.addEventListener("change", function() {
        const selectedOriginalName = this.value;
        fetchVideoData(selectedOriginalName);
    });
});

(function($) {

	skel.breakpoints({
		xlarge:	'(max-width: 1680px)',
		large:	'(max-width: 1280px)',
		medium:	'(max-width: 980px)',
		small:	'(max-width: 736px)',
		xsmall:	'(max-width: 480px)'
	});

	$(function() {

		var	$window = $(window),
			$body = $('body');

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');

			$window.on('load', function() {
				window.setTimeout(function() {
					$body.removeClass('is-loading');
				}, 100);
			});

		// Fix: Placeholder polyfill.
			$('form').placeholder();

		// Prioritize "important" elements on medium.
			skel.on('+medium -medium', function() {
				$.prioritize(
					'.important\\28 medium\\29',
					skel.breakpoint('medium').active
				);
			});

		// Off-Canvas Navigation.

			// Navigation Panel Toggle.
				$('<a href="#navPanel" class="navPanelToggle"></a>')
					.appendTo($body);

			// Navigation Panel.
				$(
					'<div id="navPanel">' +
						$('#nav').html() +
						'<a href="#navPanel" class="close"></a>' +
					'</div>'
				)
					.appendTo($body)
					.panel({
						delay: 500,
						hideOnClick: true,
						hideOnSwipe: true,
						resetScroll: true,
						resetForms: true,
						side: 'left'
					});

			// Fix: Remove transitions on WP<10 (poor/buggy performance).
				if (skel.vars.os == 'wp' && skel.vars.osVersion < 10)
					$('#navPanel')
						.css('transition', 'none');

	});

})(jQuery);