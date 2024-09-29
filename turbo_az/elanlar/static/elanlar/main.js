document.addEventListener("DOMContentLoaded", function() {
    const heartIcons = document.querySelectorAll(".card .icon");
    
    heartIcons.forEach(icon => {
        const favourites = JSON.parse(localStorage.getItem("favourites")) ?? []
        const heartId = icon.closest(".card").id

        favourites.forEach(favourite => {
            if(favourite.id === heartId) {
                icon.classList.add("active")
            }
        })

        icon.addEventListener("click", function() {
            this.classList.toggle("active");

            const currentCard = icon.closest(".card")

             const carImg = currentCard.querySelector(".car-img").src
             const carBrand = currentCard.querySelector(".badge").textContent
             const carModel = currentCard.querySelector(".car-model").textContent
             const carPrice = currentCard.querySelector(".price").textContent
             const carLocation = currentCard.querySelector(".car-location").textContent
             const carInfo = currentCard.querySelector(".car-info").textContent

             const carDetails = {
                carBrand,
                carImg,
                carInfo,
                carLocation,
                carModel,
                carPrice,
                id: currentCard.id
             }

             let favouriteCars = JSON.parse(localStorage.getItem("favourites")) || []

             const existingCar = favouriteCars.find(car => car.id === carDetails.id) ?? null

             if(favouriteCars.length === 0) {
                 favouriteCars = [carDetails]
                 saveToLocal(favouriteCars, "favourites")
             } else if(existingCar) {
                favouriteCars = favouriteCars.filter(car => car.id !== carDetails.id)
                saveToLocal(favouriteCars, "favourites")
             } else {
                favouriteCars = [...favouriteCars, carDetails]
                saveToLocal(favouriteCars, "favourites")
             }
        });
    });
});

const saveToLocal = (item, itemName) => localStorage.setItem(itemName, JSON.stringify(item)) 

const myText = document.querySelector('.myText');
const btn = document.querySelector('.btns');

function showBtn() {
    if (myText.classList.contains('show')) {
        myText.classList.remove('show');
        setTimeout(() => {
            myText.style.display = 'none';
        }, 300); 
        btn.textContent = 'Show';
    } else {
        myText.style.display = 'block';
        setTimeout(() => {
            myText.classList.add('show');
        }, 20); 
        btn.textContent = 'Hide';
    }
    console.log('salam');
}

btn.addEventListener('click', showBtn);