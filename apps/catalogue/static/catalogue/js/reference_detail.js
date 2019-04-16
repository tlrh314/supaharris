function retrieve_reference(pk) {
    $.ajax({ 
        type: 'GET', 
        url: '/api/v1/catalogue/reference/' + pk + '?format=datatables', 
        dataType: 'json',
        success: function(reference) {
            if (reference.data.ads_url.toLowerCase().includes('arxiv.org')) {
                var ads_or_arxiv = 'arXiv';
            } else if (reference.data.ads_url.toLowerCase().includes('ads')) {
                var ads_or_arxiv = 'ADS';
            } else {
                var ads_or_arxiv = 'URL';
            }
            var r = new Array(), n = -1;
            r[++n] = '<tbody>';
            r[++n] = '<tr><th>Title</th><td>' + reference.data.title + '</td></tr>';
            r[++n] = '<tr><th>Frirst Author</th><td>' + reference.data.first_author + '</td></tr>';
            r[++n] = '<tr><th>Authors</th><td>' + reference.data.authors + '</td></tr>';
            r[++n] = '<tr><th>Journal</th><td>' + reference.data.journal + '</td></tr>';
            r[++n] = '<tr><th>Year</th><td>' + reference.data.year + '</td></tr>';
            r[++n] = '<tr><th>Month</th><td>' + reference.data.month + '</td></tr>';
            r[++n] = '<tr><th>Volume</th><td>' + reference.data.volume + '</td></tr>';
            r[++n] = '<tr><th>Pages</th><td>' + reference.data.pages + '</td></tr>';
            r[++n] = '<tr><th>DOI</th><td><a target="_blank" href="' + reference.data.doi + '">' + reference.data.doi + '</a></td></tr>';
            r[++n] = '<tr><th>External URL</th><td><a target="_blank" href="' + reference.data.ads_url + '">' + ads_or_arxiv + '</a>'  + '</td></tr>';
            r[++n] = '</tbody>';
            $('#reference').html(r.join('')); 
        }
    });
}
