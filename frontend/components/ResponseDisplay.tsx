'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Copy, 
  Share2, 
  Bookmark, 
  Heart, 
  Clock, 
  Play,
  ExternalLink,
  CheckCircle
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface ResponseDisplayProps {
  response: any
  isDevotion: boolean
}

export function ResponseDisplay({ response, isDevotion }: ResponseDisplayProps) {
  const [copied, setCopied] = useState<string | null>(null)
  const { toast } = useToast()

  const handleCopy = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(type)
      toast({
        title: "Copied!",
        description: `${type} copied to clipboard`,
      })
      setTimeout(() => setCopied(null), 2000)
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to copy to clipboard",
        variant: "destructive",
      })
    }
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Abide: Christian AI Companion',
          text: 'Check out this spiritual guidance from Abide',
          url: window.location.href,
        })
      } catch (err) {
        // User cancelled sharing
      }
    } else {
      // Fallback to copying link
      handleCopy(window.location.href, 'link')
    }
  }

  const handleBookmark = () => {
    toast({
      title: "Bookmarked!",
      description: "Response saved to your bookmarks",
    })
  }

  if (isDevotion) {
    return <DevotionDisplay response={response} />
  }

  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
          Here's your personalized guidance
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Based on your feelings about: <span className="font-medium">{response.topic}</span>
        </p>
      </div>

      {/* Bible Verses */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Heart className="w-5 h-5 text-red-500" />
            <span>Bible Verses</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {response.verses?.map((verse: any, index: number) => (
            <div key={index} className="space-y-2">
              <div className="flex items-start justify-between">
                <Badge variant="secondary" className="text-xs">
                  {verse.translation}
                </Badge>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleCopy(verse.text, 'verse')}
                  className="h-8 w-8 p-0"
                >
                  {copied === `verse-${index}` ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </Button>
              </div>
              <blockquote className="text-lg text-gray-700 dark:text-gray-300 italic border-l-4 border-blue-500 pl-4">
                "{verse.text}"
              </blockquote>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                — {verse.reference}
              </p>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Reflection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Bookmark className="w-5 h-5 text-blue-500" />
            <span>Reflection</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {response.reflection}
          </p>
          <div className="mt-4 flex justify-end">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleCopy(response.reflection, 'reflection')}
              className="flex items-center space-x-2"
            >
              {copied === 'reflection' ? (
                <CheckCircle className="w-4 h-4 text-green-500" />
              ) : (
                <Copy className="w-4 h-4" />
              )}
              <span>Copy</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Prayer */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Heart className="w-5 h-5 text-red-500" />
            <span>Prayer</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed italic">
            {response.prayer}
          </p>
          <div className="mt-4 flex justify-end">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleCopy(response.prayer, 'prayer')}
              className="flex items-center space-x-2"
            >
              {copied === 'prayer' ? (
                <CheckCircle className="w-4 h-4 text-green-500" />
              ) : (
                <Copy className="w-4 h-4" />
              )}
              <span>Copy</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-3 justify-center">
        <Button
          onClick={handleShare}
          variant="outline"
          className="flex items-center space-x-2"
        >
          <Share2 className="w-4 h-4" />
          <span>Share</span>
        </Button>
        
        <Button
          onClick={handleBookmark}
          variant="outline"
          className="flex items-center space-x-2"
        >
          <Bookmark className="w-4 h-4" />
          <span>Save</span>
        </Button>
      </div>
    </div>
  )
}

function DevotionDisplay({ response }: { response: any }) {
  const [copied, setCopied] = useState<string | null>(null)
  const { toast } = useToast()

  const handleCopy = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(type)
      toast({
        title: "Copied!",
        description: `${type} copied to clipboard`,
      })
      setTimeout(() => setCopied(null), 2000)
    } catch (err) {
      toast({
        title: "Error",
        description: "Failed to copy to clipboard",
        variant: "destructive",
      })
    }
  }

  const formatDuration = (seconds: number) => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
          Your 10-Minute Devotion Plan
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Theme: <span className="font-medium capitalize">{response.theme}</span>
        </p>
      </div>

      {/* Opening Prayer */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Heart className="w-5 h-5 text-red-500" />
            <span>Opening Prayer (1 min)</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed italic">
            {response.plan.opening_prayer}
          </p>
        </CardContent>
      </Card>

      {/* Scripture Reading */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Bookmark className="w-5 h-5 text-blue-500" />
            <span>Scripture Reading (3-4 min)</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {response.plan.scriptures?.map((verse: any, index: number) => (
            <div key={index} className="space-y-2">
              <div className="flex items-start justify-between">
                <Badge variant="secondary" className="text-xs">
                  {verse.translation}
                </Badge>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleCopy(verse.text, `verse-${index}`)}
                  className="h-8 w-8 p-0"
                >
                  {copied === `verse-${index}` ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </Button>
              </div>
              <blockquote className="text-lg text-gray-700 dark:text-gray-300 italic border-l-4 border-blue-500 pl-4">
                "{verse.text}"
              </blockquote>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                — {verse.reference}
              </p>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Reflection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Bookmark className="w-5 h-5 text-green-500" />
            <span>Reflection (3 min)</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {response.plan.reflection}
          </p>
        </CardContent>
      </Card>

      {/* Action Steps */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-orange-500" />
            <span>Action Steps</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {response.plan.action_steps?.map((step: string, index: number) => (
              <li key={index} className="flex items-start space-x-3">
                <span className="w-6 h-6 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-sm font-medium mt-0.5">
                  {index + 1}
                </span>
                <span className="text-gray-700 dark:text-gray-300">{step}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Closing Prayer */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Heart className="w-5 h-5 text-red-500" />
            <span>Closing Prayer (1 min)</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed italic">
            {response.plan.closing_prayer}
          </p>
        </CardContent>
      </Card>

      {/* YouTube Video */}
      {response.video && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Play className="w-5 h-5 text-red-500" />
              <span>Related Content</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="aspect-video bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden">
                <img
                  src={response.video.thumbnailUrl}
                  alt={response.video.title}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="space-y-2">
                <h3 className="font-medium text-gray-900 dark:text-white">
                  {response.video.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {response.video.channelTitle}
                  {response.video.duration && (
                    <span className="ml-2 text-gray-500">
                      • {formatDuration(response.video.duration)}
                    </span>
                  )}
                </p>
                <Button
                  onClick={() => window.open(`https://www.youtube.com/watch?v=${response.video.videoId}`, '_blank')}
                  className="w-full bg-red-600 hover:bg-red-700 text-white"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Watch on YouTube
                  <ExternalLink className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Timer and Action Buttons */}
      <div className="space-y-4">
        <div className="text-center">
          <Button
            size="lg"
            className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-8 py-3"
          >
            <Clock className="w-5 h-5 mr-2" />
            Start 10-Minute Timer
          </Button>
        </div>
        
        <div className="flex flex-wrap gap-3 justify-center">
          <Button variant="outline" onClick={() => handleCopy(JSON.stringify(response, null, 2), 'devotion')}>
            <Copy className="w-4 h-4 mr-2" />
            Copy Plan
          </Button>
          <Button variant="outline">
            <Bookmark className="w-4 h-4 mr-2" />
            Save Devotion
          </Button>
        </div>
      </div>
    </div>
  )
}
