const selectPackage = (packageName) => {
    document.getElementById("payment-modal").style.display = "flex";
    document.getElementById("selectedPackage").innerText = `You selected: ${packageName}`;
    
}

const closeModal = (modalId) => {
    document.getElementById(modalId).style.display = "none";
}

const initiatePayment = () => {
    const phoneNumber = document.getElementById("phone-number").value;
    if (!phoneNumber){
        alert("Please enter your phone number to initiate Mpesa payment");
        return;
    }
    closeModal('payment-modal');
    const processingModel = document.getElementById("processing-modal");
    processingModel.style.display = "flex";
    setTimeout(()=>{
        processingModel.style.display = "none";
        const successModal = document.getElementById("success-modal");
        successModal.style.display = "flex";
        setTimeout(()=> closeModal('success-modal'), 5000);
    }, 5000);
}