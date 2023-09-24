const bank = document.getElementById("bank");
const username = document.getElementById("username");
const password = document.getElementById("password");
const checkBalance = document.getElementById("checkBalance");
const rewardsBalance = document.getElementById("rewardsBalance");
const redeemBalance = document.getElementById("redeemBalance");
const redeem = document.getElementById("redeem");
const redeemStatus = document.getElementById("redeemStatus");

const apiBaseUrl = "https://swype-api.onrender.com/";
const startTaskBranch = "start_task"
const taskStatusBranch = "check_task_status/"

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

if (checkBalance) {
    checkBalance.addEventListener('click', async () => {
        console.log("here1");
        rewardsBalance.innerHTML = "Checking your rewards balance, this make take a minute..."
        var taskId = await startTaskGetBalance();
        console.log(taskId);
        var data = await checkTaskStatus(taskId);
        console.log(data);
        if (data !== null) {
            rewardsBalance.innerHTML = `Rewards Balance: $${data.rewards_balance}`;
        } else {
            rewardsBalance.innerHTML = "An error occurred. Please try again later."
        }
    })
}

if (redeem) {
    redeem.addEventListener('click', async () => {
        rewardsBalance.innerHTML = "Redeeming your rewards, this make take a minute..."
        var data = await startTaskRedeemRewards();
        if (data !== null) {
            rewardsBalance.innerHTML = `Successfully redeemed $${redeemBalance.value}!`;
        } else {
            rewardsBalance.innerHTML = "An error occurred. Please try again later."
        }
    })
}

// Begin a task to check rewards balance
async function startTaskGetBalance() {
    const getBalanceUrl = apiBaseUrl + startTaskBranch;
    fetch(getBalanceUrl, {
            method: "POST",
            body:{"bank": bank.value, "task_type": "check_balance", "username": username.value, "password":password.value}
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return data.task_id;
        })
        .catch(error => {
            console.error('Error:', error);
            return null;
        });
}

// Begin a task to check rewards balance
async function startTaskRedeemRewards() {
    const redeemRewardsUrl = apiBaseUrl + redeemBranch
    fetch(redeemRewardsUrl)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            return data.task_id;
        })
        .catch(error => {
            console.error('Error:', error);
            return null;
        });
}

// Begin a task to redeem rewards balance
async function checkTaskStatus(taskId) {
    const checkTaskStatusUrl = apiBaseUrl + taskStatusBranch + taskId;
    fetch(checkTaskStatusUrl)
        .then(response => response.json())
        .then(async data => {
            if (data !== null) {
                // Valid response received, handle the data
                console.log('Received valid response:', data);
                return data;
            } else {
                // Retry after a delay (e.g., 2 seconds)
                setTimeout(await checkTaskStatus(taskId), 2000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            return null;
        });
}
