const form = document.getElementById('warrantyForm');
const warrantyTable = document.getElementById('warrantyTable').querySelector('tbody');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const equipment_id = document.getElementById('equipment_id').value;
    const equipment_name = document.getElementById('equipment_name').value;
    const warranty_period = document.getElementById('warranty_period').value;
    const purchase_date = document.getElementById('purchase_date').value;

    const response = await fetch('/add_warranty', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ equipment_id, equipment_name, warranty_period, purchase_date }),
    });
    const data = await response.json();
    alert(data.message);
    loadWarranties();
});

async function loadWarranties() {
    const response = await fetch('/list_warranties');
    const data = await response.json();
    warrantyTable.innerHTML = data.warranties.map(w => `
        <tr>
            <td>${w.equipment_id}</td>
            <td><input type="text" value="${w.equipment_name}" data-id="${w._id}" class="editable-name"></td>
            <td><input type="text" value="${w.warranty_period}" data-id="${w._id}" class="editable-period"></td>
            <td><input type="date" value="${w.purchase_date}" data-id="${w._id}" class="editable-date"></td>
            <td>${w.expiration_date}</td>
            <td>
                <button onclick="deleteWarranty('${w._id}')">Delete</button>
            </td>
        </tr>
    `).join('');
    attachEditListeners();
}

function attachEditListeners() {
    document.querySelectorAll('.editable-name, .editable-period, .editable-date').forEach(input => {
        input.addEventListener('change', async (e) => {
            const id = e.target.getAttribute('data-id');
            const field = e.target.className.includes('name') ? 'equipment_name' :
                e.target.className.includes('period') ? 'warranty_period' : 'purchase_date';
            const value = e.target.value;

            await fetch(`/update_warranty/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ [field]: value })
            });
            loadWarranties();
        });
    });
}

async function deleteWarranty(id) {
    await fetch(`/delete_warranty/${id}`, { method: 'DELETE' });
    loadWarranties();
}

loadWarranties();
