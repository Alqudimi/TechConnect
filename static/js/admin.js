// Admin Dashboard Functionality

function viewInquiry(inquiryId, message) {
    const modal = document.getElementById('inquiryModal');
    const messageElement = document.getElementById('inquiryMessage');
    
    messageElement.textContent = message;
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('inquiryModal');
    modal.style.display = 'none';
}

function deleteInquiry(inquiryId) {
    if (confirm('Are you sure you want to delete this inquiry?')) {
        fetch(`/admin/inquiry/${inquiryId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Inquiry deleted successfully');
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting inquiry');
        });
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('inquiryModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}