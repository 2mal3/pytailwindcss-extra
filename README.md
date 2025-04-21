# pytailwindcss-extra

Use _Tailwind CSS_ **with daisyUI** without _Node.js_ and install it via pip.

> An extension of [pytailwindcss](https://github.com/timonweb/pytailwindcss) with [tailwind-cli-extra](https://github.com/dobicinaitis/tailwind-cli-extra)
> to enable [daisyUI](https://daisyui.com/) support.

## Why

_Tailwind CSS_ is notoriously dependent on _Node.js_. If you're a _Python_ developer, this dependency may not be welcome
in your team, your Docker container, or your inner circle.

The _Tailwind CSS_ team recently announced a new standalone CLI build that gives you the full power of _Tailwind CLI_ in
a self-contained executable — no _Node.js_ or `npm` required.

However, installing such a standalone CLI isn't as easy as running `npm install`, the installation command for _Node.js_.

So the user [timonweb](https://github.com/timonweb) created the [pytailwindcss](https://github.com/timonweb/pytailwindcss)
package, which allows you to install the standalone Tailwind CLI with a simple `pip` command.

While this package works well, there is one particular problem. Due to the binary nature of the _Tailwind CLI_, only the
official _Tailwind CSS_ plugins are included and other plugins, especially the very popular _daisyUI_ plugin, cannot be
installed (see [Caveats](#caveats)).

Although the problem cannot be solved completely, _daisyUI_ is very useful, not only for me, so the user [dobicinaitis](https://github.com/dobicinaitis)
offers [tailwind-cli-extra](https://github.com/dobicinaitis/tailwind-cli-extra), a _Tailwind CLI_ binary patched with
_daisyUI_. Using this binary, pytailwindcss-extra extends _pytailwindcss_ and provides the _Tailwind CLI_ with the
_daisyUI_ plugin for the Python ecosystem.


## Get started

1. Install `tailwindcss-extra` via `pip` by executing the following command:

   ```
   pip install pytailwindcss-extra
   ```

2. The `tailwindcss-extra` command should now be available in your terminal. Try to run it:

   ```
   tailwindcss-extra
   ```

   If the installation was successful, you should see the message about binary being downloaded on the first run. When
   download is complete, you should see the help output for the `tailwindcss-extra` command. Use it to create a
   new project or work with an existing _Tailwind CSS_ project.

3. Let's create a new project. Go to the directory where you want to create your _Tailwind CSS_ project and initialize it
   by creating an CSS file e.g. `input.css`:

   ```css
   @import "tailwindcss";
   @plugin "daisyui";
   ```

4. Start a watcher by running:

   ```
   tailwindcss-extra -i input.css -o output.css --watch
   ```

5. Compile and minify your CSS for production by running:

   ```
   tailwindcss-extra -i input.css -o output.css --minify
   ```

You got it. Please refer to [official Tailwind documentation](https://tailwindcss.com/docs) for more information on
using _Tailwind CSS_ and its CLI.

## Caveats

It's not all roses, though. Giving up _Node.js_ means you won't be able to install plugins or additional dependencies
for your _Tailwind CSS_ setup. At the same time, that might not be a dealbreaker. You can still customize _Tailwind CSS_
via your CSS file. And the standalone build also comes with all official _Tailwind CSS_ plugins
like `@tailwindcss/aspect-ratio`, `@tailwindcss/forms`, `@tailwindcss/line-clamp`, `@tailwindcss/typography` and of
course `daisyUI`. So in 90% of _Tailwind CSS_ usage cases you should be covered, and the setup is so simplified now.

Here is what the _Tailwind CSS_ team says about going the standalone _Tailwind CSS_ route:
> If you’re working on a project where you don’t otherwise need _Node.js_ or `npm`, the standalone build can be a great
> choice. If Tailwind was the only reason you had a package.json file, this is probably going to feel like a nicer
> solution.
