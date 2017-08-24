var meetup = {};
meetup.init = function() {
    var backgrounds = [
        {
            name: 'background-0.jpg',
            credit: 'Family Hike by woodleywonderworks'
        },{
            name: 'background-1.jpg',
            credit: 'Ski in I Trysil by Trysil'
        },{
            name: 'background-2.jpg',
            credit: 'Hiking Auyuittuq National Park by Peter Morgan'
        },{
            name: 'background-3.jpg',
            credit: 'Death Valley Camping by Markus Spiering'
        },{
            name: 'background-4.jpg',
            credit: 'Camping Area by Earl McGehee'
        }, {
            name: 'background-5.jpg',
            credit: "U.S. Women's National Team vs. Canada by brent flanders"
        }, {
            name: 'background-6.jpg',
            credit: 'Foam Party by davideoneclick'
        }, {
            name: 'background-7.jpg',
            credit: 'Climbing Detail by arbyreed'
        }, {
            name: 'background-8.jpg',
            credit: 'Ice Hockey Panning by Enea Pestelacci'
        }

    ];

    var index = Math.floor((Math.random() * 10)) % 8;
    $('body').css('background', $('body').css('background').replace(/background-./, 'background-'+ index));
    $('#photo-credit').text('Photo Credit - ' + backgrounds[index].credit);
}

$(document).ready(function() {
    meetup.init();
});