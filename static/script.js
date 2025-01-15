const selectPackage = (packageName) => {
    document.getElementById("payment-section").style.display = "block";
    document.getElementById("selectedPackage").innerText = `You selected: ${packageName}`;
}

const initiatePayment = () => {
    const phoneNumber = document.getElementById("phone-number").ariaValueMax;
    if (!phoneNumber){
        alert("Please enteryour phone number to initiate Mpesa payment");
        return;
    }
    document.getElementById("payment-section").innerHTML = "<p>Processing Payment ...Please wait as we verity.</p>";
    setTimeout(()=>{
        document.getElementById("success-animation").style.display = "block";
    },5000)
}