const bank = document.getElementById("bank");
const username = document.getElementById("username");
const password = document.getElementById("password");
const checkBalance = document.getElementById("checkBalance");
const rewardsBalance = document.getElementById("rewardsBalance");

const apiBaseUrl = "https://swype-api.onrender.com/";
const getBalanceBranch = "get_rewards_balance"
const redeemBranch = "redeem_rewards"
const taskStatusBranch = "check_task_status/"

checkBalance.addEventListener('click', async () => {
    rewardsBalance.innerHTML = "Checking your rewards balance, this make take a minute..."
    var taskId = await startTaskGetBalance();
    var data = await checkTaskStatus(taskId);
    if (data !== null) {
        rewardsBalance.innerHTML = `Rewards Balance: ${data}`;
    } else {
        rewardsBalance.innerHTML = "An error occurred. Please try again later."
    }
})

// Begin a task to check rewards balance
async function startTaskGetBalance() {
    const getBalanceUrl = apiBaseUrl + getBalanceBranch
    fetch(getBalanceUrl)
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
