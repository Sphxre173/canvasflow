const STATUS_MAP = {
    "sketch": 20,
    "sketch_review": 40,
    "coloring": 60,
    "final_review": 80,
    "completed": 100
};

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".progress_bar").forEach(function(bar) {
        let status = bar.dataset.status;

        //<button class="accept_button action" onclick="request_update({{ work.info[0] }}, 'pending')">ACCEPT</button>
        let percent = STATUS_MAP[status] || 0;

        bar.style.width = percent + "%";
    });
});
