(function($) {
    $(document).ready(function() {

        generateID()
        choose()
        generateOption()
        selectionOption()
        removeClass()
        uploadImage()
        submit()
        resetButton()
        removeNotification()
        autoRemoveNotification()
        autoDequeue()

        var ID
        var way = 0
        var queue = []
        var fullStock = 10
        var speedCloseNoti = 1000

        function generateID() {
            var text = $('header span')
            var newID = ''

            for (var i = 0; i < 3; i++) {
                newID += Math.floor(Math.random() * 3)
            }

            ID = 'ID: 5988' + newID
            text.html(ID)
        }

        function choose() {
            var li = $('.ways li')
            var section = $('.sections section')
            var index = 0
            li.on('click', function() {
                index = $(this).index()
                $(this).addClass('active')
                $(this).siblings().removeClass('active')

                section.siblings().removeClass('active')
                section.eq(index).addClass('active')
                if (!way) {
                    way = 1
                } else {
                    way = 0
                }
            })
        }

        function generateOption() {
            var select = $('select option')
            var selectAdd = $('.select-option .option')
            $.each(select, function(i, val) {
                $('.select-option .option').append('<div rel="' + $(val).val() + '">' + $(val).html() + '</div>')
            })
        }

        function selectionOption() {
            var select = $('.select-option .head')
            var option = $('.select-option .option div')

            select.on('click', function(event) {
                event.stopPropagation()
                $('.select-option').addClass('active')
            })

            option.on('click', function() {
                var value = $(this).attr('rel')
                $('.select-option').removeClass('active')
                select.html(value)

                $('select#category').val(value)
            })
        }

        function removeClass() {
            $('body').on('click', function() {
                $('.select-option').removeClass('active')
            })
        }

        function uploadImage() {
            var button = $('.images .pic')
            var uploader = $('<input type="file" accept="image/*" />')
            var images = $('.images')

            button.on('click', function() {
                uploader.click()
            })

            uploader.on('change', function() {
                var reader = new FileReader()
                reader.onload = function(event) {
                    images.prepend('<div class="img" style="background-image: url(\'' + event.target.result + '\');" rel="' + event.target.result + '"><span>remove</span></div>')
                }
                reader.readAsDataURL(uploader[0].files[0])

            })

            images.on('click', '.img', function() {
                $(this).remove()
            })

        }

        function submit() {
            var button = $('#send')

            button.on('click', function() {
                var name = $('#name')
                var model = $('#model')
                var floor = $('#floor')
                var type = $('#type')
                var images = $('.images .img')
                var imageArr = []

                for (var i = 0; i < images.length; i++) {
                    imageArr.push({ url: $(images[i]).attr('rel') })
                }

                var newStock = {
                    name: name.val(),
                    model: model.val(),
                    floor: floor.val(),
                    images: imageArr,
                    type: type.val()
                }

                saveToQueue(newStock)

            })
        }

        function removeNotification() {
            var close = $('.notification')
            close.on('click', 'span', function() {
                var parent = $(this).parent()
                parent.fadeOut(300)
                setTimeout(function() {
                    parent.remove()
                }, 300)
            })
        }

        function autoRemoveNotification() {
            setInterval(function() {
                var notification = $('.notification')
                var notiPage = $(notification).children('.btn')
                var noti = $(notiPage[0])

                setTimeout(function() {
                    setTimeout(function() {
                        noti.remove()
                    }, speedCloseNoti)
                    noti.fadeOut(speedCloseNoti)
                }, speedCloseNoti)
            }, speedCloseNoti)
        }

        function autoDequeue() {
            var notification = $('.notification')
            var text

            setInterval(function() {

                if (queue.length > 0) {
                    if (queue[0].type == 2) {
                        text = ' Your discusstion is sent'
                    } else {
                        text = ' Your order is allowed.'
                    }

                    notification.append('<div class="success btn"><p><strong>Success:</strong>' + text + '</p><span><i class=\"fa fa-times\" aria-hidden=\"true\"></i></span></div>')
                    queue.splice(0, 1)

                }
            }, 10000)
        }

        function resetButton() {
            var resetbtn = $('#reset')
            resetbtn.on('click', function() {
                reset()
            })
        }

        // helpers
        function saveToQueue(stock) {
            var notification = $('.notification')
            var check = 0

            if (queue.length <= fullStock) {
                if (!stock.name || !stock.model || !stock.floor || stock.images == 0) {
                    check = 1
                }
                console.log(stock.name + stock.model + stock.type + stock.floor)
            }

            if (check) {
                notification.append('<div class="error btn"><p><strong>Error:</strong> Please fill in the form.</p><span><i class=\"fa fa-times\" aria-hidden=\"true\"></i></span></div>')
            } else {
                notification.append('<div class="success btn"><p><strong>Success:</strong> ' + ID + ' is submitted.</p><span><i class=\"fa fa-times\" aria-hidden=\"true\"></i></span></div>')

                $.ajax({
                    url: '/adminm',
                    type: 'POST',
                    data: { 'name': stock.name, 'model': stock.model, 'type': stock.type, 'floor': stock.floor, 'images': stock.images },
                    success: function(response) {
                        notification.append('<div class="success btn"><p><strong>Success:</strong> ' + ID + ' is pushed.</p><span><i class=\"fa fa-times\" aria-hidden=\"true\"></i></span></div>')
                        location.reload();

                    }
                })
                queue.push(stock)
                reset()
            }
        }

        function reset() {

            $('#title').val('')
            $('.select-option .head').html('Floor')
            $('select#category').val('')
            $('#name').val('')
            $('#model').val('')
            $('#type').val('')
            var images = $('.images .img')
            for (var i = 0; i < images.length; i++) {
                $(images)[i].remove()
            }

            var topic = $('#topic').val('')
            var message = $('#msg').val('')
        }
    })

})(jQuery)

function manage(id, name, model, type, floor) {
    console.log(id)
    Swal.fire({
        title: name,
        text: "Modello: " + model + " | Tipo: " + type + " | Piano: " + floor,
        icon: 'info',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Cancella Il macchinario',
        cancelButtonText: 'Annulla',
    }).then((result) => {
        if (result.value) {

            $.ajax({
                url: '/deleteImg',
                type: 'POST',
                data: { 'id': id },
                success: function(response) {
                    Swal.fire(
                        'Cancellato!',
                        'Il Macchinario è stato eliminato.',
                        'success',
                    ).then((result) => {
                        if (result.value) {
                            location.reload();

                        }
                    })

                }
            })

        }

    })
}