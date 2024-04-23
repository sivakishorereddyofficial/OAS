

let otpVerifyBtn = document.querySelector('#otpBtn')
console.log('{{csrf_token}}')

const get_cookies = () => {
    let cookies = document.cookie.split(";")
    let objs = {}
    cookies.forEach(cookie => {
        let [name, val] = cookie.split("=")
        objs[name.trim()] = val.trim()
    });
    return objs
}

otpVerifyBtn.onclick = async (e) => {
    let otpUserInput = document.querySelector('#otpUserInput').value

    console.log(otpUserInput.value)

    let res = await fetch('verify-otp', {
        method : "POST", 
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": '{{csrf_token}}'
          },
        body :  JSON.stringify({"otp": otpUserInput})
    })
    let jsonRes = await res.json()
    console.log(jsonRes)
    if(jsonRes?.status){
        window.location.href = jsonRes?.redirect_url
    }
    else{
        alert(jsonRes?.detail)
    }
}




