显示 Opencv 的 Mat 图片：
```kotlin
class ImageViewer(windowName: String, width: Int, height: Int) {
    private var imageView: JLabel? = null
    private var frame: JFrame

    init {
        frame = createJFrame(windowName, width, height)
        frame.pack()
        frame.setLocationRelativeTo(null)
        frame.isVisible = true
        frame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE// 用户点击窗口关闭
    }


    /**
     * 图片显示
     */
    fun imshow(img: Mat) {
        setSystemLookAndFeel()
        val loadedImage = toBufferedImage(img)
        imageView!!.icon = ImageIcon(loadedImage)
    }

    private fun setSystemLookAndFeel() {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName())
        } catch (e: ClassNotFoundException) {
            e.printStackTrace()
        } catch (e: InstantiationException) {
            e.printStackTrace()
        } catch (e: IllegalAccessException) {
            e.printStackTrace()
        } catch (e: UnsupportedLookAndFeelException) {
            e.printStackTrace()
        }

    }

    private fun createJFrame(windowName: String, width: Int, height: Int): JFrame {
        val frame = JFrame(windowName)
        imageView = JLabel()
        val imageScrollPane = JScrollPane(imageView)
        imageScrollPane.preferredSize = Dimension(width, height)
        frame.add(imageScrollPane, BorderLayout.CENTER)
        frame.defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE
        return frame
    }


    private fun toBufferedImage(matrix: Mat?): Image {
        var type = BufferedImage.TYPE_BYTE_GRAY
        if (matrix!!.channels() > 1) {
            type = BufferedImage.TYPE_3BYTE_BGR
        }
        val bufferSize = matrix.channels() * matrix.cols() * matrix.rows()
        val buffer = ByteArray(bufferSize)
        matrix.get(0, 0, buffer) // 获取所有的像素点
        val image = BufferedImage(matrix.cols(), matrix.rows(), type)
        val targetPixels = (image.raster.dataBuffer as DataBufferByte).data
        System.arraycopy(buffer, 0, targetPixels, 0, buffer.size)
        return image
    }
}
```
