




$(document).ready(function () {

           //SIDE MENU SCRIPTS
    
            $('.menu-close-icon').click(function (e) {
                e.preventDefault();
                $('#side-menu').animate({ left: '-250px'});
               
            });

            $('.menu-open-icon').click(function (e) {
                e.preventDefault();
                var left = $('#side-menu').offset().left
                if (left == -250) {
                    $('#side-menu').animate({ left: '0px', top: '0px' });
                }
                else {
                    $('#side-menu').animate({ left: '-250px'});
                }
               
            });

   

            /*====================================
             WRITE YOUR   SCRIPTS  BELOW
            ======================================*/

   });



