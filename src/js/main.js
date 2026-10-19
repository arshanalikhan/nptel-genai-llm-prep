/* Start-up. Every module above only defines things; this file runs them, in this order. */

Theme.init();
Practice.init();
MustKnow.init();
MockExams.init();
Home.updateCountdowns();
Videos.init();        // before Notes, so the "Watch" button sits right under each week's heading
Numericals.init();
Notes.init();
Router.init();        // shows the page for the current URL
drawIcons();
