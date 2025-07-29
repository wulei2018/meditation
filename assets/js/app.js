const { createApp } = Vue

const app = createApp({
    data() {
        return {
            durations: [3, 5, 10, 15, 20, 30],
            selectedDuration: 5,
            styles: [
                'Mindfulness Meditation',
                'Breathing Meditation',
                'Guided Meditation',
                'Body Scan',
                'Loving-Kindness Meditation'
            ],
            selectedStyle: 'Mindfulness Meditation',
            currentVideo: null,
            videoPlayer: null,
            availableVideos: {},
            faqs: [
                {
                    question: 'Can I meditate at any time of the day?',
                    answer: 'Yes! The beauty of 5-minute meditation is its flexibility. You can practice in the morning, during lunch break, or in the evening. Just choose a time when you won\'t be disturbed.'
                },
                {
                    question: 'Which meditation style is best for beginners?',
                    answer: 'For beginners, we recommend starting with "Guided Meditation". It provides voice guidance to help you maintain focus and learn the basics of meditation.'
                },
                {
                    question: 'How do I maintain focus during meditation?',
                    answer: 'It\'s normal for your mind to wander. When you notice this happening, gently bring your attention back to your breath. This process of returning focus is actually part of the meditation practice.'
                },
                {
                    question: 'Why choose 5 minutes?',
                    answer: '5 minutes is an excellent starting point that doesn\'t feel overwhelming but can still provide real benefits. As you become more comfortable, you can gradually increase the duration.'
                },
                {
                    question: 'Do I need a special posture?',
                    answer: 'Not necessarily. You can sit cross-legged, in a chair, or even lie down. The most important thing is to maintain a comfortable and relaxed position.'
                }
            ]
        }
    },
    async mounted() {
        await this.loadAvailableVideos();
        this.initializeVideoPlayer();
        this.setRandomVideo();
        this.initializeGiscus();
    },
    methods: {
        initializeGiscus() {
            // 创建giscus script元素
            const script = document.createElement('script');
            script.src = 'https://giscus.app/client.js';
            script.setAttribute('data-repo', 'wulei2018/meditation');
            script.setAttribute('data-repo-id', 'R_kgDOPUH_yg');
            script.setAttribute('data-category', 'Announcements');
            script.setAttribute('data-category-id', 'DIC_kwDOPUH_ys4CthSD');
            script.setAttribute('data-mapping', 'pathname');
            script.setAttribute('data-strict', '0');
            script.setAttribute('data-reactions-enabled', '1');
            script.setAttribute('data-emit-metadata', '0');
            script.setAttribute('data-input-position', 'bottom');
            script.setAttribute('data-theme', 'preferred_color_scheme');
            script.setAttribute('data-lang', 'en');
            script.setAttribute('crossorigin', 'anonymous');
            script.async = true;

            // 找到评论容器并添加script
            const giscusContainer = document.querySelector('.giscus');
            if (giscusContainer) {
                giscusContainer.innerHTML = '';
                giscusContainer.appendChild(script);
            }
        },
        async loadAvailableVideos() {
            // 在实际项目中，这个信息应该从服务器获取
            // 这里我们直接硬编码可用的视频
            this.availableVideos = {
                3: Array.from({length: 13}, (_, i) => i + 1),  // 1-13
                5: Array.from({length: 13}, (_, i) => i + 1),
                10: Array.from({length: 13}, (_, i) => i + 1),
                15: Array.from({length: 13}, (_, i) => i + 1),
                20: Array.from({length: 13}, (_, i) => i + 1),
                30: Array.from({length: 13}, (_, i) => i + 1)
            };
        },
        initializeVideoPlayer() {
            this.videoPlayer = videojs('meditation-video', {
                controls: true,
                autoplay: false,
                preload: 'auto',
                fluid: true,
                responsive: true
            });
        },
        getRandomVideo(duration) {
            const videos = this.availableVideos[duration] || [];
            if (videos.length === 0) return null;
            
            const randomIndex = Math.floor(Math.random() * videos.length);
            const videoNumber = videos[randomIndex];
            return `assets/videos/${duration}min/${videoNumber}.mp4`;
        },
        setRandomVideo() {
            const newVideo = this.getRandomVideo(this.selectedDuration);
            if (newVideo && this.videoPlayer) {
                this.currentVideo = newVideo;
                this.videoPlayer.src({ type: 'video/mp4', src: newVideo });
                this.videoPlayer.load();
            }
        },
        shuffleVideo() {
            this.setRandomVideo();
            if (this.videoPlayer) {
                this.videoPlayer.play();
            }
        }
    },
    watch: {
        selectedDuration(newDuration) {
            this.setRandomVideo();
        },
        selectedStyle(newStyle) {
            // 目前风格改变时也随机换视频
            this.setRandomVideo();
        }
    }
})

app.mount('#app') 