module.exports = {
  title: 'Darkness',
   description: 'The fastest way to get started with NeoPixels!',
   themeConfig: {
      logo: '/logo.png',

      head: [
        ['link', { rel: "icon", type: "image/png", href: "/favicon.png"}],
        ['meta', { name: "theme-color", content: "#f9d32d"}],
      ],

      repo: 'rangerdigital/darkness',
      repoLabel: 'GitHub',
      docsDir: 'docs',
      editLinks: true,
      editLinkText: 'Help me improve this page!',
      nav: [
         { text: 'Home', link: '/' },
         { text: 'Guide', link: '/guide/' },
      ],
   },
   sidebar: 'auto',
}
