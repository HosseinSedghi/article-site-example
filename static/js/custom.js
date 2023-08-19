function articleCommentReplay(commentId, commentAuthor) {
    $('#comment-replay').val(commentId);
    document.getElementById('comment-replay-text').innerHTML = `@ پاسخ برای <span>${commentAuthor}</span>`;
    document.getElementById("comment-replay-box").scrollIntoView();
    window.scrollTo();
}


function deleteComment(commentId) {
    Swal.fire({
        title: 'حذف کامنت',
        text: "آیا از حذف کامنت مطمئن هستید؟",
        icon: 'warning',
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'بله. حذف شود'
    }).then((result) => {
        if (result.isConfirmed) {
            $.get('comment-delete', {
                comment_id: commentId
            }).then(res => {
                if (res.status === 'success') {
                    location.reload();
                }
            })
        }
    })
}

function convertCommentToPublish(commentId) {
    $.get('convert-comment-to-publish', {
        comment_id: commentId
    }).then(res => {
        $('#comment-box').html(res);
    })
}

function convertCommentToDraft(commentId) {
    $.get('convert-comment-to-draft', {
        comment_id: commentId
    }).then(res => {
        $('#comment-box').html(res);
    })
}

function addArticleToSlider(articleId) {
    $.get('', {
        article_add_slider: articleId
    }).then(res => {
        $('#article-box').html(res);
    })
}

function deleteArticleOfSlider(articleId) {
    $.get('', {
        article_delete_slider: articleId
    }).then(res => {
        $('#article-box').html(res);
    })
}

function deleteTicket(ticketId) {
    Swal.fire({
        title: 'حذف تیکت',
        text: "آیا از حذف تیکت مطمئن هستید؟",
        icon: 'warning',
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'بله. حذف شود'
    }).then((result) => {
        if (result.isConfirmed) {
            $.get('delete-ticket', {
                ticket_id: ticketId
            }).then(res => {
                if (res.status === 'success') {
                    location.reload();
                }
            })
        }
    })
}
