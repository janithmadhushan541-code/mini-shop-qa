# Finish external evidence on Windows
1. Open project in VS Code with Node 22. Run `npm install` (refresh lockfile), `npm run coverage`, `npm run build`, `npm run dev`.
2. Capture terminal coverage and browser catalog. Install Selenium using `pip install selenium`; run `python tests/selenium_ui.py` while dev server runs.
3. Push to GitHub; Actions > Mini Shop QA > successful run; capture screenshot. Create issues from QA-REPORT and record actual transitions.
4. JMeter: create Thread Group (10 users, ramp 5 seconds, loop 10), HTTP Request GET localhost:5173 /, Summary Report and Aggregate Report. Run against local server only; save .jmx and screenshot metrics.
5. SonarQube: start local instance, create mini-shop project and token; run SonarScanner from project root with SONAR_TOKEN environment variable and local server URL. Capture overview and issues. Coverage import requires LCOV generation separately; native text report is not LCOV.
6. Implement/run Cucumber step definitions, perform manual UI/security checks and update report. Do not submit pending items as passed.
