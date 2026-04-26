const API = "";   // 🔥 IMPORTANT FIX

console.log("✅ SCRIPT LOADED");

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    let formData = new FormData();
    formData.append("customer_id", document.getElementById("customer_id").value);
    formData.append("old_name", document.getElementById("old_name").value);
    formData.append("new_name", document.getElementById("new_name").value);
    formData.append("file", document.getElementById("file").files[0]);

    await fetch(`${API}/submit`, {
        method: "POST",
        body: formData
    });

    alert("Submitted!");
    await loadPending();
});

async function loadPending() {
    let res = await fetch(`${API}/pending`);
    let data = await res.json();

    console.log("📊 DATA RECEIVED:", data);

    let table = document.querySelector("#pendingTable tbody");
    table.innerHTML = "";

    data.forEach(item => {
        let row = document.createElement("tr");

        row.innerHTML = `
            <td>${item.request_id}</td>
            <td>${item.customer_id}</td>
            <td>${item.confidence_score}</td>
            <td>${item.summary}</td>
            <td>
                <button onclick="approve('${item.request_id}')">Approve</button>
                <button onclick="reject('${item.request_id}')">Reject</button>
            </td>
        `;

        table.appendChild(row);
    });
}

async function approve(id) {
    await fetch(`${API}/approve/${id}`, { method: "POST" });
    await loadPending();
}

async function reject(id) {
    await fetch(`${API}/reject/${id}`, { method: "POST" });
    await loadPending();
}

window.onload = loadPending;