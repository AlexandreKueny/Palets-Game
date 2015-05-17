$(document).ready(function() {
    $('#games').dataTable( {
        "ajax": 'data.json',
        "columns": [
            { "data": "id" },
            { "data": "date" },
            { "data": "duree" },
            { "data": "Joueur A" },
            { "data": "Joueur B" },
            { "data": "points" },
			{ "data": "but A" },
			{ "data": "but B" }
        ]
    } );
	$('#stats').dataTable( {
        "ajax": 'data.json',
        "columns": [
            { "stats": "games tot" },
            { "stats": "time tot" },
            { "stats": "points tot" }
        ]
    } );
} );