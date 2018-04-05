from Action import *

class ActionFactory(object):

    @staticmethod
    def moveBy(deltaX, deltaY, duration):
        def run(target, deltaTime, totalTime):
            target.moveBy(deltaX/duration * deltaTime, deltaY/duration * deltaTime)
            return (totalTime >= duration)
        return Action(run)
    
    @staticmethod
    def rotateBy(deltaAngle, duration):
        def run(target, deltaTime, totalTime):
            target.rotateBy(deltaAngle/duration * deltaTime)
            return (totalTime >= duration)
        return Action(run)

    @staticmethod
    def fadeOut(duration):
        def run(target, deltaTime, totalTime):
            # print( target.opacity )
            target.opacity = 1 - totalTime/duration
            if (target.opacity < 0):
                target.opacity = 0
            return (totalTime >= duration)
        return Action(run)

    @staticmethod
    def fadeIn(duration):
        def run(target, deltaTime, totalTime):
            target.opacity = totalTime/duration
            if (target.opacity > 1):
                target.opacity = 1
            return (totalTime >= duration)
        return Action(run)

    @staticmethod
    def sequence(*args):
        actionList = list(args)
        currentIndex = 0
        sequenceAction = Action()
        def apply(target, deltaTime):
            nonlocal currentIndex
            currentAction = actionList[currentIndex]
            finished = currentAction.apply(target, deltaTime)
            if (finished):
                currentIndex += 1
            return (currentIndex == len(actionList))
        def reset():
            nonlocal currentIndex
            for action in actionList:
                action.reset()
            currentIndex = 0
        sequenceAction.apply = apply
        sequenceAction.reset = reset
        return sequenceAction

    @staticmethod
    def repeat(action, totalTimes):
        finishedTimes = 0
        repeatAction = Action()
        def apply(target, deltaTime):
            finished = action.apply(target, deltaTime)
            if (finished):
                finishedTimes += 1
                action.reset()
            return (finishedTimes == totalTimes)
        repeatAction.apply = apply
        return repeatAction

    @staticmethod
    def forever(action):
        foreverAction = Action()
        def apply(target, deltaTime):
            finished = action.apply(target, deltaTime)
            if (finished):
                action.reset()
            return False
        foreverAction.apply = apply
        return foreverAction

    @staticmethod
    def delay(duration):
        def run(target, deltaTime, totalTime):
            return (totalTime >= duration)
        return Action(run)
    
    @staticmethod
    def remove():
        def run(target, deltaTime, totalTime):
            target.remove()
            return True
        return Action(run)


    @staticmethod
    def boundToScreen(screenWidth, screenHeight):
        def run(target, deltaTime, totalTime):
            target.boundToScreen(screenWidth, screenHeight)
            return False
        return Action(run)

    @staticmethod
    def wrapToScreen(screenWidth, screenHeight):
        def run(target, deltaTime, totalTime):
            target.wrapToScreen(screenWidth, screenHeight)
            return False
        return Action(run)

    @staticmethod
    def destroyOutsideScreen(screenWidth, screenHeight):
        def run(target, deltaTime, totalTime):
            if not target.isOnScreen(screenWidth, screenHeight):
                target.remove()
                return True
            else:
                return False
        return Action(run)


    @staticmethod
    def isAnimationFinished():
        def run(target, deltaTime, totalTime):
            return target.animation.isFinished()
        return Action(run)

    
