function articleCommentReplay(commentId, commentAuthor) {
    $('#comment-replay').val(commentId);
    if (commentAuthor.first_name) {
        document.getElementById('comment-replay-text').innerHTML = commentAuthor.first_name;
    } else {
        document.getElementById('comment-replay-text').innerHTML = commentAuthor.username;
    }
}

function deleteCategory(categoryId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
            )
        }
    })
}