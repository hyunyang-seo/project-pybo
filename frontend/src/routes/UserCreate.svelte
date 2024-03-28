<script>
    import { push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import Error from "../componets/Error.svelte";

    let error = { detail: [] };
    let username = "";
    let password1 = "";
    let password2 = "";
    let email = "";

    function post_user(event) {
        event.preventDefault();
        let url = "/api/user/create";
        let params = {
            username: username,
            password1: password1,
            password2: password2,
            email: email,
        };
        fastapi(
            "post",
            url,
            params,
            (json) => {
                push("/user-login");
            },
            (json_error) => {
                error = json_error;
            },
        );
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">Sign up</h5>
    <Error {error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">User name</label>
            <input
                type="text"
                class="form-control"
                id="username"
                bind:value={username}
            />
        </div>
        <div class="mb-3">
            <label for="password1">Password</label>
            <input
                type="password"
                class="form-control"
                id="password1"
                bind:value={password1}
            />
        </div>
        <div class="mb-3">
            <label for="password2">Password confirm</label>
            <input
                type="password"
                class="form-control"
                id="password2"
                bind:value={password2}
            />
        </div>
        <div class="mb-3">
            <label for="email">Email</label>
            <input
                type="text"
                class="form-control"
                id="email"
                bind:value={email}
            />
        </div>
        <button type="submit" class="btn btn-primary" on:click={post_user}
            >Create</button
        >
    </form>
</div>
