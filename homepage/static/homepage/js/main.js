//self invoking function
(function()
{
    //get input1 by id
    var inp1 = document.getElementById('inp1');

    //get input2 by id
    var inp2 = document.getElementById('inp2');

    //get form by id
    var form = document.getElementById('form-s');

    //get backend reply variables
    var myVar = document.getElementById("myVar").value;
    myVar = JSON.parse(myVar);

    if (myVar.login === 0){
        alert("Invalid User Or Password");
    }

    else if(myVar.login === 1)
    {
        
        // Get modal element
        var modal = document.getElementById('modal1');
    
        // Get open modal button
        var modalbtn = document.getElementById("modal-btn");
    
        //Get Close
        var closebtn = document.getElementById('clseBtn');

        // Get capture button
        var captureButton = document.getElementById('capbt');

        //get authentication form
        var aut_form = document.getElementById("aut-form");

        // listen to open click
        openModal();

        Webcam.set({
            image_format: 'jpeg',
            jped_quality: 90,
        })

        Webcam.attach('vid-vid');

        // listen to close click
        closebtn.addEventListener("click", closeModal);
    
        // listen for outside click
        window.addEventListener("click", outsideClick);
    
        // listen to captor click
        captureButton.addEventListener("click",captureimg);

        
        aut_form.onsubmit = function(e){

            //prevent form from behaving in its default setting
            e.preventDefault();

        }

        //get authenticationn submit botton by id
        var auth_sub_btn = document.getElementById("aut-sub");



        // listen to authenticator submit botton click
        auth_sub_btn.addEventListener("click",submitimgs);

        if (myVar.prediction === 0){
            document.getElementById("modal2").style.display = 'block';
            
            retry = document.getElementById("retry")
            retry.addEventListener('click',()=>{
                document.getElementById("modal2").style.display = 'none';
            })

        }
        //function to open Modal
        function openModal()
        {
            modal.style.display = 'block';
        }
                    
        //function to close modal
        function closeModal()
        {
            modal.style.display = 'none';
            document.reload(forceGet=True)
        }

        //funtion to close modal when there is a click outside the box
        function outsideClick(e)
        {
            if(e.target == modal){
                modal.style.display = 'none';
                document.reload(forceGet=True)
            }
        }

        //funtion to capture image
        function captureimg(){

            Webcam.snap(function(data_url){
                var sub_btn = document.getElementById("aut-img2");
                sub_btn.value = data_url;
                document.getElementById('result').innerHTML = "<img class='img2' width='300' src='"+data_url+ "'>";

            })

        }

        //funtion to submit images
        function submitimgs(){

            var sub_btn2 = document.getElementById("aut-img2");
            document.getElementById("aut-img1").value = myVar.username;
            console.log(document.getElementById("aut-img1").value);

            if (sub_btn2.value === ''){
                alert('Capture an Image Of you To Proceed');
            }

            else{
                aut_form.submit();
            }
        }

        aut_form.reset();
    }
        
    form.reset();

    // prevents page from resubmitting form
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
      }
})();