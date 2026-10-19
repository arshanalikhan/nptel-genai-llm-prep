/* Site-wide settings.
 * COURSE, QUESTIONS, MUST_KNOW and VIDEOS are defined in data.js, which tools/build.py generates from data/.
 *
 * Saved progress lives in the reader's browser (localStorage) under keys that start with STORAGE_KEY.
 * Changing STORAGE_KEY, or reordering the question files, would make returning readers lose their answers. */

const SITE_NAME = "NPTEL GenAI & LLMs Prep";
const STORAGE_KEY = "genprep-v1";
const THEME_KEY = "genprep-theme";          // also read by the inline script in <head>
const WEEK_COUNT = COURSE.weeks.length;
const EXAM_DAY = COURSE.examDate;           // "YYYY-MM-DD", India time
const PASS_MARK = 40;                        // raw score out of 100 that equals the 30/75 exam pass mark
const PAPER_SIZE = 50;                       // questions per mock paper (2 marks each)
const PAPER_SECONDS = 3 * 60 * 60;           // 3-hour mock papers
const LETTERS = "ABCDEF";                    // option labels
