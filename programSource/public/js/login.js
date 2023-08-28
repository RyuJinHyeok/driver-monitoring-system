/*
    By June K. 2023/08/22
*/


const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");

user_id = 'admin'
user_pwd = 'admin1'

loginButton.addEventListener("click", (event) => {
    event.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === user_id && password === user_pwd) {
        alert("로그인 성공! 시스템 페이지로 이동합니다.");
        location.href="index.html";
    } else {
        alert("비밀번호가 틀렸습니다. 다시 입력해주세요.");
    }
});