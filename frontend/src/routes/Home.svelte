<script>
    import fastapi from "../lib/api";
    import { link } from "svelte-spa-router";
    import { page, keyword, is_login } from "../lib/store";
    import moment from "moment/min/moment-with-locales";
    moment.locale("en");

    let question_list = [];
    let size = 10;
    let total = 0;
    let kw = "";
    $: total_page = Math.ceil(total / size);

    function get_question_list(_page) {
        let params = {
            page: $page,
            size: size,
            keyword: $keyword,
        };
        fastapi("get", "/api/question/list", params, (json) => {
            question_list = json.question_list;
            total = json.total;
            kw = $keyword;
        });
    }

    $: $page, $keyword, get_question_list();
</script>

<div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            <a
                use:link
                href="/question-create"
                class="btn btn-primary {$is_login ? '' : 'disabled'}"
                >Submit question</a
            >
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value={kw} />
                <button
                    class="btn btn-outline-secondary"
                    on:click={() => {
                        ($keyword = kw), ($page = 0);
                    }}
                >
                    Search
                </button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
            <tr class="text-center table-dark">
                <th>Number</th>
                <th style="width: 50%;">Title</th>
                <th>Author</th>
                <th>Creation date and time</th>
            </tr>
        </thead>
        <tbody>
            {#each question_list as question, i}
                <tr class="text-center">
                    <td>{total - $page * size - i}</td>
                    <td class="text-start">
                        <a use:link href="/detail/{question.id}"
                            >{question.subject}</a
                        >
                        {#if question.answers.length > 0}
                            <span class="text-danger small mx-2"
                                >{question.answers.length}</span
                            >
                        {/if}
                    </td>
                    <td>{question.user ? question.user.username : ""}</td>
                    <td
                        >{moment(question.create_date).format(
                            "YYYY-MM-DD hh:mm:ss A",
                        )}
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
    <!-- Start paging processing -->
    <ul class="pagination justify-content-center">
        <!-- Back page -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click={() => $page--}>Back</button>
        </li>
        <!-- Page numbering -->
        {#each Array(total_page) as _, loop_page}
            {#if loop_page >= $page - 5 && loop_page <= $page + 5}
                <li class="page-item {loop_page === $page && 'active'}">
                    <button
                        on:click={() => ($page = loop_page)}
                        class="page-link">{loop_page + 1}</button
                    >
                </li>
            {/if}
        {/each}
        <!-- Next page -->
        <li class="page-item {$page >= total_page - 1 && 'disabled'}">
            <button class="page-link" on:click={() => $page++}>Next</button>
        </li>
    </ul>
    <!-- End of paging processing -->
</div>
