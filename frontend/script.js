document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const submitBtn = document.getElementById('submit-btn');
    const resultBox = document.getElementById('result-box');
    const resultFilename = document.getElementById('result-filename');
    const resultStatus = document.getElementById('result-status');
    const resultSummary = document.getElementById('result-summary');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset UI
        submitBtn.disabled = true;
        submitBtn.innerText = '處理中...';
        resultBox.style.display = 'none';

        const formData = new FormData(form);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            // Update UI with Data
            resultFilename.innerText = `分析結果：${data.filename}`;
            resultSummary.textContent = data.summary;

            // Handle Notion Status
            if (data.notion_status && data.notion_status.includes('Success')) {
                resultStatus.className = 'status-tag status-success';
                resultStatus.innerText = 'Notion 同步成功';
            } else {
                resultStatus.className = 'status-tag status-error';
                resultStatus.innerText = data.notion_status || '未知錯誤';
            }

            resultBox.style.display = 'block';

        } catch (error) {
            console.error('Error:', error);
            alert('上傳發生錯誤，請稍後再試。');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = '上傳並分析';
        }
    });
});
