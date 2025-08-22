'use client'

import { AlertTriangle, Phone, ExternalLink, Heart } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

interface CrisisBannerProps {
  message: string
  supportiveVerses: any[]
  prayer: string
  resources: string[]
}

export function CrisisBanner({ message, supportiveVerses, prayer, resources }: CrisisBannerProps) {
  return (
    <div className="space-y-6">
      {/* Crisis Alert */}
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="w-6 h-6 text-red-600 dark:text-red-400 mt-1 flex-shrink-0" />
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-red-800 dark:text-red-200">
              Crisis Support Available
            </h3>
            <p className="text-red-700 dark:text-red-300 leading-relaxed">
              {message}
            </p>
          </div>
        </div>
      </div>

      {/* Supportive Bible Verses */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-red-600 dark:text-red-400">
            <Heart className="w-5 h-5" />
            <span>Words of Comfort</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {supportiveVerses?.map((verse: any, index: number) => (
            <div key={index} className="space-y-2">
              <div className="flex items-start justify-between">
                <Badge variant="secondary" className="text-xs">
                  {verse.translation}
                </Badge>
              </div>
              <blockquote className="text-lg text-gray-700 dark:text-gray-300 italic border-l-4 border-red-500 pl-4">
                "{verse.text}"
              </blockquote>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                — {verse.reference}
              </p>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Prayer */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-red-600 dark:text-red-400">
            <Heart className="w-5 h-5" />
            <span>Prayer for You</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed italic">
            {prayer}
          </p>
        </CardContent>
      </Card>

      {/* Crisis Resources */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-red-600 dark:text-red-400">
            <Phone className="w-5 h-5" />
            <span>Immediate Help & Resources</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {resources?.map((resource, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <Phone className="w-4 h-4 text-red-500 flex-shrink-0" />
                <span className="text-gray-700 dark:text-gray-300 text-sm">
                  {resource}
                </span>
              </div>
            ))}
          </div>
          
          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">
              Remember:
            </h4>
            <ul className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
              <li>• You are not alone in this</li>
              <li>• Help is available 24/7</li>
              <li>• Your life has value and meaning</li>
              <li>• God loves you unconditionally</li>
            </ul>
          </div>
        </CardContent>
      </Card>

      {/* Additional Support */}
      <div className="text-center space-y-4">
        <p className="text-gray-600 dark:text-gray-400 text-sm">
          If you're in immediate danger, please call 911 or go to your nearest emergency room.
        </p>
        
        <div className="flex flex-wrap gap-3 justify-center">
          <Button
            variant="outline"
            onClick={() => window.open('https://988lifeline.org', '_blank')}
            className="border-red-300 text-red-600 hover:bg-red-50 dark:border-red-700 dark:text-red-400 dark:hover:bg-red-900/20"
          >
            <ExternalLink className="w-4 h-4 mr-2" />
            988 Lifeline
          </Button>
          
          <Button
            variant="outline"
            onClick={() => window.open('https://www.crisistextline.org', '_blank')}
            className="border-red-300 text-red-600 hover:bg-red-50 dark:border-red-700 dark:text-red-400 dark:hover:bg-red-900/20"
          >
            <ExternalLink className="w-4 h-4 mr-2" />
            Crisis Text Line
          </Button>
        </div>
      </div>
    </div>
  )
}
