function validateForm() {
    // Get the input element by its ID
    var name = document.getElementById("name");
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    
    // Check if any of inputs are null
    if (!name.value.trim() || !username.value.trim() || !password.value.trim()) {
        alert("Please enter values for all fields");
        return false; // Prevent form submission
    }

    // If all inputs are not null, allow form submission
    return true;
}

// ensure that your script runs after the DOM is fully loaded. 
document.addEventListener("DOMContentLoaded", function() {
    // 查詢會員姓名
    document.getElementById('searchbutton').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent form submission or default behavior
        const username = document.getElementById('searchname').value; // Fetch the value from 'searchname' input field
        fetch(`/api/member?username=${encodeURIComponent(username)}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('searchresult');
            if (data.data) {
                resultDiv.innerHTML = `<p>${data.data.name} (${data.data.username})</p>`;
            } else {
                resultDiv.innerHTML = `<p>No Data</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // 更新我的姓名
    const updatename=document.getElementById('updatename');
    const updatebutton=document.getElementById('updatebutton');

    updatebutton.addEventListener('click',()=>{
        const newname=updatename.value;
        if (!newname){
            return;
        }

        fetch('/api/member',{
            method:'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body:JSON.stringify({name:newname}) // Convert the new name to a JSON string and include it in the request body
        })

        .then(response=>{
            if (!response.ok){
                // 檢查回應的狀態碼，如果是 200 表示成功，否則拋出一個錯誤
                throw new Error('Failed to Update');
            }
            return response.json();
        })
        .then(data=>{
            const resultDiv = document.getElementById('updateresult');
            if (data.ok){
                resultDiv.innerHTML = `<p>Updated</p>`;

                // 更新會員頁歡迎訊息
                const welcome=document.getElementById('welcome');
                welcome.textContent=`${newname}，\n歡迎登入系統`;
            }else{
                resultDiv.innerHTML = `<p>Failed to Update</p>`;
            }
        })
    })
});

function backtohome(){
    window.location.href = "http://127.0.0.1:8000";
}

function signout(){
    window.location.href = "http://127.0.0.1:8000/signout";
}