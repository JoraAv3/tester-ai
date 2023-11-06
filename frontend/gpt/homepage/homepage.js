let filebtn = document.querySelector(".filebtn");
let leftside = document.querySelector(".leftside");
let leftbody = document.querySelector(".leftbody");
let righteside = document.querySelector(".righteside");
let textenter = document.querySelector(".textenter");
let masagesub = document.querySelector(".masagesub");
let masagesub2 = document.querySelector(".masagesub2");
let secondmasagebox = document.querySelector(".secondmasagebox");
let githubrepos = document.querySelector(".githubrepos");
let login = document.querySelector(".login");
let singup = document.querySelector(".singup");
let login2 = document.querySelector(".login2");
let logincancle = document.querySelector(".logincancle");
let formoffersingup = document.querySelector(".formoffersingup");
let offerlogin = document.querySelector(".offerlogin");
let logout = document.querySelector(".logout ");
let pass = document.querySelector(".pass");
let pass3 = document.querySelector(".pass3");
let yourcodebtn = document.querySelector(".yourcodebtn");
let yourcodebtn2 = document.querySelector(".yourcodebtn2");
let githubblock1 = document.querySelector(".githubblock1");
let githubblock2 = document.querySelector(".githubblock2");
let githubblock3 = document.querySelector(".githubblock3");
let codemanage = document.querySelector(".codemanage");
let yourcode = document.querySelector(".yourcode");
let signup = document.querySelector("#signup");
let signin = document.querySelector("#signin");
let loggoogle = document.querySelector(".loggoogle");
let paybtn = document.querySelector(".paybtn");
let paywrapper = document.querySelector(".paywrapper");
let paycancle = document.querySelector(".paycancle");
let payWind = document.querySelector(".payWind");
const API_HOST = "http://127.0.0.1:8000";

filebtn.addEventListener("click", function myFunction() {
  leftside.classList.toggle("left100");
  righteside.classList.toggle("right0");
  textenter.classList.toggle("textenterbig");
  masagesub.classList.toggle("masagesubbig");
});

masagesub.addEventListener("click", function myFunction(e) {
  if (textenter.value) {
    addMessageToList({ text: textenter.value, question_id: undefined });
  }
});

const api_fetch = (url, method, data = null) => {
  const token = localStorage.getItem("token");
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const _url = new URL(url);
  if (method === "GET") {
    _url.search = new URLSearchParams(data).toString();
  }
  const payload = method === "GET" ? {} : { body: JSON.stringify(data) };
  return fetch(_url, {
    ...payload,
    method: method,
    cors: "no-cors",
    headers: {
      ...headers,
      "Content-type": "application/json",
      "Access-Control-Allow-Origin": "*/*",
    },
  });
};

const registerWithGoogle = (code, data) => {
  const url = `${API_HOST}/auth/google/callback`;
  data.code = code;
  return api_fetch(url, "POST", data).then((response) => response.json());
};

githubblock1.addEventListener("click", function myFunction() {
  githubblock1.classList.remove("githubblock1");
  githubblock1.classList.add("none");
  githubblock2.classList.remove("githubblock2");
  githubblock2.classList.add("none");
  githubblock3.classList.remove("githubblock3");
  githubblock3.classList.add("none");
  codemanage.style.opacity = "1";
  githubrepos.style.display = "block";
});

githubblock2.addEventListener("click", function myFunction() {
  githubblock1.classList.remove("githubblock1");
  githubblock1.classList.add("none");
  githubblock2.classList.remove("githubblock2");
  githubblock2.classList.add("none");
  githubblock3.classList.remove("githubblock3");
  githubblock3.classList.add("none");
  codemanage.style.opacity = "1";
  githubrepos.style.display = "block";
});

githubblock3.addEventListener("click", function myFunction() {
  githubblock1.classList.remove("githubblock1");
  githubblock1.classList.add("none");
  githubblock2.classList.remove("githubblock2");
  githubblock2.classList.add("none");
  githubblock3.classList.remove("githubblock3");
  githubblock3.classList.add("none");
  codemanage.style.opacity = "1";
  yourcode.style.display = "block";
});

codemanage.addEventListener("click", function myfunc() {
  githubblock1.classList.remove("none");
  githubblock1.classList.add("githubblock1");
  githubblock2.classList.remove("none");
  githubblock2.classList.add("githubblock2");
  githubblock3.classList.remove("none");
  githubblock3.classList.add("githubblock3");
  codemanage.style.opacity = "0";
  githubrepos.style.display = "none";
  yourcode.style.display = "none";
});

login.addEventListener("click", function loginfun() {
  login2.style.display = "block";
  offerlogin.style.borderBottom = "2px solid #7c7f87";
  formoffersingup.style.borderBottom = "none";
  signin.style.display = "block";
  signup.style.display = "none";
});

singup.addEventListener("click", function loginfun3() {
  login2.style.display = "block";
  offerlogin.style.borderBottom = "none";
  formoffersingup.style.borderBottom = "2px solid #7c7f87";
  signin.style.display = "none";
  signup.style.display = "block";
});

logincancle.addEventListener("click", function loginfun3() {
  login2.style.display = "none";
});

offerlogin.addEventListener("click", function loginfun() {
  offerlogin.style.borderBottom = "2px solid #7c7f87";
  formoffersingup.style.borderBottom = "none";
  signin.style.display = "block";
  signup.style.display = "none";
});

formoffersingup.addEventListener("click", function loginfun() {
  offerlogin.style.borderBottom = "none";
  formoffersingup.style.borderBottom = "2px solid #7c7f87";
  signin.style.display = "none";
  signup.style.display = "block";
});
//

masagesub2.addEventListener("click", () => {
  login2.style.display = "block";
  offerlogin.style.borderBottom = "2px solid #7c7f87";
  formoffersingup.style.borderBottom = "none";
  signin.style.display = "block";
  signup.style.display = "none";
});

yourcodebtn2.addEventListener("click", () => {
  login2.style.display = "block";
  offerlogin.style.borderBottom = "2px solid #7c7f87";
  formoffersingup.style.borderBottom = "none";
  signin.style.display = "block";
  signup.style.display = "none";
});

//
signup.addEventListener("submit", function signupAction(event) {
  event.preventDefault();
  const formData = new FormData(signup);
  const data = Object.fromEntries(formData);
  console.log("forData", data, formData);
  api_fetch(`${API_HOST}/signup`, "POST", data)
    .then((response) => response.json())
    .then((response_data) => {
      const { token_id: token } = response_data;
      console.log("token", token);
      console.log("response_data", response_data);
      if (!token) {
        throw new Error(response_data.detail);
      }
      localStorage.setItem("token", token);
      login2.style.display = "none";
      singup.style.display = "none";
      login.style.display = "none";
      logout.style.display = "inline-block";
      masagesub.style.display = "inline-block";
      masagesub2.style.display = "none";
      yourcodebtn.style.display = "inline-block";
      yourcodebtn2.style.display = "none";
      paybtn.style.display = "inline-block";
      return response_data;
    })
    .catch((err) => {
      document.querySelector(".invalidmail").style.opacity = "1";
      localStorage.removeItem("token");
    });
});

signin.addEventListener("submit", function signupAction(event) {
  event.preventDefault();
  const formData = new FormData(signin);
  const data = Object.fromEntries(formData);
  console.log("forData", data, formData);
  api_fetch(`${API_HOST}/signin`, "POST", data)
    .then((response) => response.json())
    .then((response_data) => {
      const { token_id: token } = response_data;
      console.log("token", token);
      console.log("response_data", response_data);
      if (!token) {
        throw new Error(response_data.detail);
      }
      localStorage.setItem("token", token);
      login2.style.display = "none";
      singup.style.display = "none";
      login.style.display = "none";
      logout.style.display = "inline-block";
      masagesub.style.display = "inline-block";
      masagesub2.style.display = "none";
      yourcodebtn.style.display = "inline-block";
      yourcodebtn2.style.display = "none";
      paybtn.style.display = "inline-block";
      check_user();
      return response_data;
    })
    .catch((err) => {
      document.querySelector(".invalidPass").style.opacity = "1";
      localStorage.removeItem("token");
    });
});

pass.addEventListener("click", function passchange(e) {
  document.querySelector(".invalidPass").style.opacity = "0";
});

pass3.addEventListener("click", function passchange(e) {
  document.querySelector(".invalidmail").style.opacity = "0";
});
function removetoken(params) {
  localStorage.removeItem("token");
  singup.style.display = "inline-block";
  login.style.display = "inline-block";
  logout.style.display = "none";
}

logout.addEventListener("click", function logout() {
  if (localStorage.getItem("token")) {
    removetoken();
    yourcodebtn.style.display = "none";
    yourcodebtn2.style.display = "inline-block";
    masagesub.style.display = "none";
    masagesub2.style.display = "inline-block";
    paybtn.style.display = "none";
    window.location.reload();
  }
});

function onSuccess(googleUser) {
  console.log("Logged in as: " + googleUser.getBasicProfile().getName());
  var profile = googleUser.getBasicProfile();
  console.log("ID: " + profile.getId());
  console.log("Full Name: " + profile.getName());
  console.log("Email: " + profile.getEmail());

  var id_token = googleUser.getAuthResponse().id_token;
  console.log("ID Token: " + id_token);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", `${API_HOST}/auth/google`);
  xhr.setRequestHeader("Content-Type", 'application/json;charset=UTF-8"');
  xhr.onload = function () {
    console.log("Signed in as: " + xhr.responseText);
  };
  xhr.send(
    JSON.stringify({
      token: id_token,
      avatar: profile.getImageUrl(),
      email: profile.getEmail(),
    })
  );
}

function onFailure(error) {
  console.log(error);
}

window.addEventListener("load", (event) => {
  url = new URL(
    "http://localhost:5500/frontend/gpt/homepage/homepage.html?code=123456"
  );
  code = url.searchParams.get("code");
  if (code) {
  }
});

function onSignin(response) {
  const responsePayload = decodeJwtResponse(response.credential);

  console.log("ID: " + responsePayload.sub);
  console.log("Jti: " + responsePayload.jti);
  console.log("Email: " + responsePayload.email);

  const url = `${API_HOST}/registeration/google`;
  const data = {
    id: responsePayload.sub,
    jti: responsePayload.jti,
    email: responsePayload.email,
  };

  api_fetch(url, "POST", data)
    .then((response) => response.json())
    .then((response_data) => {
      console.log("Response from server:", response_data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  var loggitElement = document.querySelectorAll(".loggit");
  if (loggitElement.length > 0) {
    loggitElement.forEach((element) => {
      element.onclick = function () {
        location.href = `${API_HOST}/github-login`;
      };
    });
  }
  var token = localStorage.getItem("token");
  if (token) {
    check_user();
  }
});

function check_user() {
  api_fetch(`${API_HOST}/check-user`, "GET")
    .then((response) => {
      if (!response.ok) {
        throw new Error();
      }
      return response.json();
    })
    .then((data) => {
      console.log("check_user", data);
      data.forEach((message) => addMessageToList(message));
      login2.style.display = "none";
      singup.style.display = "none";
      login.style.display = "none";
      logout.style.display = "inline-block";
      masagesub.style.display = "inline-block";
      masagesub2.style.display = "none";
      yourcodebtn.style.display = "inline-block";
      yourcodebtn2.style.display = "none";
      paybtn.style.display = "inline-block";
    })
    .catch(() => {
      localStorage.removeItem("token");
    });
}

const messageForm = document.getElementById("message_form");

messageForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(event);
  return false;
});

function sendMessage(event) {
  const input = document.getElementById("message");
  const message = input.value;

  const data = {
    text: message,
  };

  api_fetch(`${API_HOST}/messages/response`, "POST", data)
    .then((response) => response.json())
    .then((data) => {
      addMessageToList(data);
      console.log(data);
    })
    .catch((error) => {
      console.error("Ошибка:", error);
    });

  input.value = "";
}

function addMessageToList(message) {
  if (message !== "") {
    let li = document.createElement("li");
    let pre = document.createElement("pre");
    let code = document.createElement("code");
    li.classList.add("leftmasagenew2");
    li.classList.add("code");
    if (message.question_id) {
      li.classList.add("answer");
    } else {
      li.classList.add("question");
    }
    code.innerHTML = message.text;
    pre.append(code);
    li.append(pre);
    secondmasagebox.append(li);
    hljs.highlightElement(code);
    leftbody.scrollTop = leftbody.scrollHeight;
  }
}

yourcodebtn.addEventListener("click", () => {
  let textarea = document.querySelector(".textarea").value;
  if (textarea) {
    addMessageToList({ text: textarea, question_id: undefined });
  }
});
paybtn.addEventListener("click", () => {
  paywrapper.style.display = "block";
  payWind.classList.remove("payMoveCancleClass");
  payWind.classList.add("payMouvClas");
});
paycancle.addEventListener("click", () => {
  payWind.classList.remove("payMouvClas");
  payWind.classList.add("payMoveCancleClass");
  setTimeout(() => {
    paywrapper.style.display = "none";
  }, 600);
});
