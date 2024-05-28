const img = document.getElementsByClassName("hero-image");
const bg = document.getElementsByClassName("hero-bg");
const audio = document.getElementById("myAudio"); // Corrected the id to "myAudio"

img[0].addEventListener("click", () => {
    if(audio.paused) {
        audio.play();
        bg[0].style.width = "100%";
        bg[0].style.animationPlayState = "running";
    audio.play();
    } else {
        audio.pause();
        bg[0].style.width = "40%";
        bg[0].style.animationPlayState = "paused";
    }
});
